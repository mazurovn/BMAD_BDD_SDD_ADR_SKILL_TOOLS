const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const boot = html.split('<script id="boot" type="application/json">')[1].split("</script>")[0];
const script = html.split("<script>\nconst STATUSES")[1];
const source = "const STATUSES" + script.split("</script>")[0];
const els = {};
function El(id) {
  this.id = id;
  this.listeners = {};
  this._value = "";
  this.textContent = "";
  this.innerHTML = "";
  this.className = "";
  this.style = {};
  this.dataset = {};
}
El.prototype.addEventListener = function (name, fn) { this.listeners[name] = fn; };
Object.defineProperty(El.prototype, "value", {
  get() { return this._value; },
  set(v) { this._value = v; },
});
Object.defineProperty(El.prototype, "options", {
  get() {
    return [...this.innerHTML.matchAll(/value="([^"]*)"/g)].map(match => ({value: match[1]}));
  },
});
const document = {
  getElementById(id) {
    if (!els[id]) els[id] = new El(id);
    return els[id];
  },
  querySelectorAll() {
    return ["backlog", "kanban", "scrum", "cycle", "architecture", "intake"].map(name => {
      const node = document.getElementById("view-" + name);
      node.classList = {toggle() {}};
      return node;
    });
  },
};
document.body = document.getElementById("body");
document.getElementById("boot").textContent = boot;
document.getElementById("q")._value = "";
document.getElementById("kind")._value = "";
document.getElementById("sprint")._value = "";
eval(source);
function click(name) { document.getElementById("view-" + name).listeners.click(); }
const checks = [];
function check(name, ok) { checks.push((ok ? "PASS " : "FAIL ") + name); }
const board = document.getElementById("view").innerHTML;
check("1 hoursOf exists", source.includes("function hoursOf"));
check("2 board shows both stories", board.includes("US-001") && board.includes("US-002"));
check("3 board has the five columns", ["backlog", "ready", "in-progress", "review", "done"].every(name => board.includes(name)));
click("architecture");
const arch = document.getElementById("view").innerHTML;
check("4 architecture svg", arch.includes("<svg") && arch.includes("CALM") && arch.includes("Sysl"));
click("cycle");
const cycle = document.getElementById("view").innerHTML;
check("5 cycle shows idea and epic", cycle.includes("IDEA-001") && cycle.includes("EPIC-001") && cycle.includes("US-001"));
const drawer = document.getElementById("drawer").innerHTML;
check("6 drawer shows acceptance and guardrails", drawer.includes("Given") && drawer.includes("Never") && drawer.includes("Гардрейлы"));
check("7 drawer shows the specification", drawer.includes("Спецификация") && drawer.includes("MUST"));
check("8 missing evidence is named", document.getElementById("gaps").textContent.includes("US-001"));
click("scrum");
const scrum = document.getElementById("view").innerHTML;
check("9 sprint shows the goal and the stories", scrum.includes("velocity") && scrum.includes("US-001") && scrum.includes("US-002"));
click("intake");
check("10 intake explains the labels", document.getElementById("view").innerHTML.includes("разобрать заметки") && document.getElementById("view").innerHTML.includes("pain"));
console.log(checks.join("\n"));
if (checks.some(line => line.startsWith("FAIL"))) process.exit(1);
