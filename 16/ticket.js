#!/usr/bin/env node

const process = require("process");
const fs = require("fs");
const { setupMaster } = require("cluster");

const USAGE = `
Usage:
${process.argv[1]} <FILENAME>
  where <FILENAME> is the path to the input file with ticket information
`

const HELP = `\
Given a file of ticket information, determine which tickets are invalid.

The file is divided into three sections, separated by blank lines.

The first section is rules indicating valid range(s) of values (inclusive)
for various named fields. Each rule is on a separate line.

The second section is "your" ticket. The ticket is a line of comma-separated
values representing field values. However, the field corresponding to each
value is unknown.

The third section is other tickets, each on a separate line in the same format
as "your" ticket. The fields are always in the same order.

https://adventofcode.com/2020/day/16
`;

class Rule {
  constructor(name, ranges) {
    this.name = name;
    this.ranges = ranges;
  }
  isValid(value) {
    return this.ranges.some(range => value >= range[0] && value <= range[1]);
  }
}

class RulesSet {
  constructor() {
    this.rules = new Map();
  }
  add(name, rule) {
    this.rules.set(name, rule);
  }
  isValid(value) {
    return Array.from(this.rules.keys()).some(name => this.rules.get(name).isValid(value));
  }
}

function parseRules(lines) {
  const rules = new RulesSet();
  for (let line of lines) {
    if (line === "") {
      break;
    }
    const [name, rangeList] = line.split(":");
    const ranges = rangeList.split("or")
      .map(rangeExpr => rangeExpr.split("-")
        .map(bound => parseInt(bound))
      );
    rules.add(name, new Rule(name, ranges));
  }
  return rules;
}

function parseTicket(line) {
  return line.split(",").map(value => parseInt(value));
}

function parseOurTicket(lines) {
  const idx = lines.findIndex(line => line === "your ticket:");
  const line = lines[idx + 1];
  return parseTicket(line);
}

function parseOtherTickets(lines) {
  let i = lines.findIndex(line => line === "nearby tickets:");
  const tickets = [];
  for (i++; i < lines.length; i++) {
    if (lines[i] === "") break;
    tickets.push(parseTicket(lines[i]));
  }
  return tickets;
}

function countErrors(tickets, rules) {
  return tickets
    .reduce((errorRate, ticket) => ticket
      .reduce((errorRate, value) => errorRate + (rules.isValid(value) ? 0 : value), errorRate),
      0
    );
}

function getValidTickets(tickets, rules) {
  return tickets.filter(ticket => ticket
    .every(value => rules.isValid(value))
  );
}

function getFieldIndices(tickets, ruleSet) {
  const indexMap = new Map();
  // Slice tickets vertically
  const indices = [];
  for (let i=0; i<tickets[0].length; i++) {
    indices[i] = i;
  }
  for (let i of indices) {
    const slice = tickets.map(ticket => ticket[i]);
    const candidates = [];
    for (const [ruleName, rule] of ruleSet.rules) {
      if (indexMap.has(ruleName)) continue;
      if (slice.every(value => rule.isValid(value))) {
        candidates.push(ruleName);
      }
    }
    if (candidates.length === 1) {
      // Unambiguous match for this slice
      indexMap.set(candidates[0], i);
    } else if (candidates.length > 1) {
      // Ambiguous - let's hope it gets disambiguated later
      // (this might create an infinite loop on evil input but ¯\_(ツ)_/¯)
      indices.push(i);
    }
  }
  return indexMap;
}

function main() {
  if (process.argv.length !== 3) {
    console.error(USAGE);
    console.error("Run with -h for more help");
    process.exitCode = 1;
    return;
  }
  if (process.argv[2] === "-h") {
    console.log(USAGE);
    console.log(HELP);
    return;
  }
  let data;
  try {
    data = fs.readFileSync(process.argv[2], "utf-8");
  } catch(ex) {
    console.error(`Couldn't open "${process.argv[2]}" (${ex})`);
    process.exitCode = 1;
    return;
  }

  const lines = data.split("\n");

  const rules = parseRules(lines);
  const ourTicket = parseOurTicket(lines);
  const otherTickets = parseOtherTickets(lines);

  const errorRate = countErrors(otherTickets, rules);
  console.log(`Error rate: ${errorRate}`);

  const validTickets = getValidTickets(otherTickets, rules);

  const fieldIndices = getFieldIndices(validTickets, rules);
  let departureFieldsProduct = 1;
  for (const [field, index] of fieldIndices) {
    if (field.indexOf("departure") === 0) {
      departureFieldsProduct *= ourTicket[index];
    }
  }
  console.log(`Product of departure fields: ${departureFieldsProduct}`);
}

main();