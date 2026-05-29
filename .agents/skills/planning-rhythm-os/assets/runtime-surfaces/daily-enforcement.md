<%*
const dailyTitle = tp.file.title;
const weekTitle = tp.date.now("GGGG-[W]WW", 0, dailyTitle, "YYYY-MM-DD");
const weekPath = `Planning/Weeks/${weekTitle}.md`;
const weekFile = app.vault.getAbstractFileByPath(weekPath);
const frontmatter = weekFile ? (app.metadataCache.getFileCache(weekFile)?.frontmatter ?? {}) : {};
const dayOfWeek = tp.date.now("dddd", 0, dailyTitle, "YYYY-MM-DD");
const isBonusWeek = frontmatter.period_type === "[[Bonus Week]]" || frontmatter.period_type === "Bonus Week";
const mode = isBonusWeek
  ? "bonus"
  : dayOfWeek === "Sunday"
    ? "review"
    : dayOfWeek === "Saturday"
      ? "lighter"
      : "execution";

const skillRoot = ".agents/skills/planning-rhythm-os/assets/runtime-surfaces";
const modeConfig = {
  bonus: {
    title: "Bonus week mode",
    callout: "important",
    summary: "Treat this as a first-class bonus week: reflection, cleanup, recovery, catch-up, vacation, or the explicitly chosen focus mode—not automatic execution.",
    extra: `Surface the bonus-week note, dates, and focus mode before planning. Focus mode: ${frontmatter.focus_mode ?? "check the week / bonus-week note"}. If urgent work overrides the bonus week, record the tradeoff explicitly.`,
    partialPath: `${skillRoot}/daily-modes/bonus-week.md`,
  },
  execution: {
    title: "Weekday execution mode",
    callout: "summary",
    summary: "Default to focused delivery, surface checks, Top 3, and protected deep work.",
    extra: "Use `planning-rhythm-os` as the canonical source of truth for execution-day workflow. [[Planning/Metacognition Control Tower]] is only a dashboard/launchpad if useful.",
    partialPath: `${skillRoot}/daily-modes/execution-day.md`,
  },
  lighter: {
    title: "Saturday lighter-day mode",
    callout: "tip",
    summary: "Default to recovery, leisure, relationships, errands, and core habits.",
    extra: "Do not assume a normal hard-core workday; if work is needed, keep it intentional and proportionate. See `planning-rhythm-os`.",
    partialPath: `${skillRoot}/daily-modes/saturday-lighter-day.md`,
  },
  review: {
    title: "Sunday closeout day",
    callout: "important",
    summary: "Determine the review stack from policy + period notes before normal daily planning.",
    extra: `Run required cadence reviews smallest → largest, then do admin/inbox cleanup. Weekly review target: [[Weekly Review - ${weekTitle}]]. Current sprint: ${frontmatter.sprint ?? "check the week note"}. Use \`planning-rhythm-os\` as canonical procedure; [[Planning/Metacognition Control Tower]] is navigation only.`, 
    partialPath: `${skillRoot}/daily-modes/sunday-review-reset.md`,
  },
};

async function readPartial(path) {
  const file = app.vault.getAbstractFileByPath(path);
  if (!file) {
    const noteRef = path.replace(/\.md$/, "");
    return `> [!error] Missing template partial: [[${noteRef}]]\n\n`;
  }
  return await app.vault.cachedRead(file);
}

const fields = {
  week: `[[${weekTitle}]]`,
  quarter: frontmatter.quarter,
  cycle: frontmatter.cycle,
  sprint: frontmatter.sprint,
  period_type: frontmatter.period_type,
  focus_mode: frontmatter.focus_mode,
  day_of_week: `[[${dayOfWeek}]]`,
};

tR += "---\n";
for (const [key, value] of Object.entries(fields)) {
  if (value) tR += `${key}: \"${value}\"\n`;
}
tR += "---\n\n";

if (!weekFile) {
  tR += `> [!error] Missing week artifact\n`;
  tR += `> Could not find [[Planning/Weeks/${weekTitle}]]. Stop and create/repair the week artifact before assuming the day's cadence fields or mode.\n\n`;
}

tR += `> [!${modeConfig[mode].callout}] ${modeConfig[mode].title}\n`;
tR += `> ${modeConfig[mode].summary}\n`;
tR += `> ${modeConfig[mode].extra}\n\n`;
tR += `> [!warning] Ritual-critical before advancing\n`;
tR += `> Before Exo moves you into execution, explicitly resolve the morning foundations for the day's mode: core habits / virtues plus the day's resurfacing items (planned/cadenced + random rediscovery when applicable). Do not let these remain implicit checklist boxes.\n\n`;

tR += await readPartial(modeConfig[mode].partialPath);
tR += "\n\n";
tR += await readPartial(`${skillRoot}/daily-modes/shared-foundations.md`);
%>
