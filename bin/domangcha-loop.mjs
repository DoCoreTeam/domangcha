#!/usr/bin/env node
// DOMANGCHA v4.0.0  bin/domangcha-loop.mjs
// 경량 설치기: 현재 작업 디렉터리에 자율개발 루프를 설치한다.
// 하네스 설치는 domangcha.sh 가 프로젝트 밖에서 판단해 맡으며, 이 파일은 ~/.claude 를 건드리지 않는다.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PKG_ROOT = path.join(__dirname, '..');
const TEMPLATES = path.join(PKG_ROOT, 'domangcha', 'loop', 'templates');
const ROOT = process.cwd();
const args = process.argv.slice(2);
const has = (f) => args.includes(f);
const optionValue = (f) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : undefined; };
const LANGS = ['ko', 'en'];
const langArg = optionValue('--lang');
if (langArg !== undefined && !LANGS.includes(langArg)) {
  console.error(`[DOMANGCHA] --lang ${LANGS.join('|')}`);
  process.exit(1);
}
const LANG = langArg || 'ko';

// 설치 시점에는 사용자 언어를 알 수 없으므로 항상 영어를 먼저, 한국어를 이어서 보여준다.
// The installer cannot know the reader's language yet, so it always shows English then Korean.
// 영어는 또렷하게, 한국어는 흐리게 — 한 화면에 둘 다 있어도 눈은 한쪽만 따라가면 된다.
// English reads bright, Korean dim: both are on screen, but the eye only follows one.
const COLOR = process.stdout.isTTY && !process.env.NO_COLOR;
const c = (code, text) => (COLOR ? `\x1b[${code}m${text}\x1b[0m` : text);
const bright = (t) => c('1;37', t);
const dim = (t) => c('2', t);
const accent = (t) => c('0;36', t);
const TAG = '[DOMANGCHA]';
const PAD = ' '.repeat(TAG.length);
const fail = (en, ko) => {
  console.error(`${accent(TAG)} ${bright(en)}`);
  if (ko) console.error(`${PAD} ${dim(ko)}`);
  process.exit(1);
};
const say = (en, ko) => {
  console.log(`${accent(TAG)} ${bright(en)}`);
  if (ko) console.log(`${PAD} ${dim(ko)}`);
};

function readVersion() {
  const f = path.join(PKG_ROOT, 'domangcha', 'VERSION');
  if (!fs.existsSync(f)) fail(`version file missing: ${f} — the package is damaged, install it again`,
    `버전 파일 없음: ${f} — 패키지가 손상되었으니 다시 설치하세요`);
  return fs.readFileSync(f, 'utf8').trim();
}
const VERSION = readVersion();

// Node 22.13 이상 필요 (node:sqlite 내장)
{
  const [maj, min] = process.versions.node.split('.').map(Number);
  if (maj < 22 || (maj === 22 && min < 13)) {
    fail(`Node 22.13+ required, found ${process.versions.node} — run nvm install 22, then try again`,
      `Node 22.13 이상 필요, 현재 ${process.versions.node} — nvm install 22 로 올린 뒤 다시 실행하세요`);
  }
}
if (!fs.existsSync(TEMPLATES)) fail(`templates missing: ${TEMPLATES}`, `템플릿 없음: ${TEMPLATES}`);

function copyIfMissing(rel) {
  const dest = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  if (fs.existsSync(dest)) return false;
  fs.copyFileSync(path.join(TEMPLATES, rel), dest);
  return true;
}
function copyAlways(rel) {
  const dest = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(path.join(TEMPLATES, rel), dest);
}

console.log('');
console.log(`  ${accent(`DOMANGCHA v${VERSION}`)} ${bright('— installing the project autonomous dev loop')}`);
console.log(`  ${' '.repeat(String(VERSION).length + 11)}${dim('프로젝트 자율개발 루프를 설치합니다')}`);
console.log(`  ${bright('target')}${dim(' / 대상')}: ${ROOT}`);
console.log('');

if (!fs.existsSync(path.join(ROOT, '.git'))) {
  try {
    execSync('git init -q', { cwd: ROOT, stdio: 'ignore' });
    say('initialised a git repository', 'git 저장소를 초기화했습니다');
  } catch (e) {
    fail(`git is required and could not run here: ${String(e.message || e).split('\n')[0]}`,
      `git 이 필요한데 실행되지 않았습니다: ${String(e.message || e).split('\n')[0]}`);
  }
}

// 기존 CLAUDE.md 자동 이관 (기본 동작, --no-migrate 로 끔)
const claudeMd = path.join(ROOT, 'CLAUDE.md');
let migrated = null;
let slimmed = false;
let importKept = false;
// 설치기가 놓은 그대로의 옛 CLAUDE.md 본문(첫 줄 버전 헤더 제외) 해시. 한 글자라도 고친 파일은 건드리지 않는다.
// Hashes of every stock old CLAUDE.md body (version header excluded); an edited file is never touched.
const STOCK_IMPORT_BODIES = new Set(['3f346074468c42f7', '48f3934a6991913a', 'c3467f51e6077f81', 'e78daa44f83f1388', 'ef5cb0d544de17a8']);
function isStockImport(text) {
  const body = text.split('\n').slice(1).join('\n');
  return STOCK_IMPORT_BODIES.has(createHash('sha256').update(body).digest('hex').slice(0, 16));
}
if (!has('--no-migrate') && fs.existsSync(claudeMd)) {
  const existing = fs.readFileSync(claudeMd, 'utf8');
  const isLoopKit = existing.includes('@LOOP.md') || /^# DOMANGCHA v3\./m.test(existing)
    || (/^# DOMANGCHA v\d/m.test(existing) && existing.includes('LOOP.md'));
  if (isLoopKit && isStockImport(existing)) {
    // 예전 판은 @LOOP.md 로 31KB 규정 전체를 매 세션 불러왔다. 손대지 않은 그 파일만 핵심판으로 바꾼다.
    // The old edition imported the whole 31KB rulebook every session; only an untouched copy is replaced.
    fs.rmSync(claudeMd);
    slimmed = true;
  } else if (isLoopKit && /^@LOOP\.md$/m.test(existing)) {
    importKept = true;
  } else if (!isLoopKit) {
    const heavyDir = path.join(ROOT, '.claude', 'heavy');
    fs.mkdirSync(heavyDir, { recursive: true });
    const dest = path.join(heavyDir, 'CEO.md');
    if (fs.existsSync(dest)) fs.rmSync(dest);
    fs.renameSync(claudeMd, dest);
    migrated = path.relative(ROOT, dest);
  }
}

// 이미 깔려 있던 판을 먼저 읽어, 갱신인지 신규인지 사람에게 분명히 알린다.
// Read the version already here first, so an update is announced as an update.
function installedLoopVersion() {
  const f = path.join(ROOT, 'scripts', 'loop.mjs');
  if (!fs.existsSync(f)) return null;
  const m = fs.readFileSync(f, 'utf8').match(/^const KIT_VERSION = "([^"]+)";$/m);
  return m ? m[1] : 'unknown';
}
const previous = installedLoopVersion();

copyAlways(path.join('scripts', 'loop.mjs')); // 항상 최신 CLI 로 갱신
const placed = [];
// 프로토콜 문서는 언어판이 따로 있고, 프로젝트에는 고른 판 하나만 놓는다.
// The protocol documents ship per language; a project receives only the edition it chose.
for (const [rel, source] of [['LOOP.md', LANG === 'en' ? 'LOOP.en.md' : 'LOOP.md'],
                             ['CLAUDE.md', LANG === 'en' ? 'CLAUDE.en.md' : 'CLAUDE.md']]) {
  const dest = path.join(ROOT, rel);
  if (!fs.existsSync(dest)) { fs.copyFileSync(path.join(TEMPLATES, source), dest); placed.push(rel); }
}
for (const rel of [
  path.join('.claude', 'commands', 'plan.md'),
  path.join('.claude', 'commands', 'loop.md'),
  path.join('.claude', 'commands', 'policy.md'),
  path.join('.cursor', 'rules', 'loop.mdc'),
]) if (copyIfMissing(rel)) placed.push(rel);

if (has('--agents')) {
  for (const link of ['AGENTS.md', 'GEMINI.md']) {
    const dest = path.join(ROOT, link);
    if (fs.lstatSync(dest, { throwIfNoEntry: false })) fs.rmSync(dest, { force: true });
    fs.symlinkSync('CLAUDE.md', dest); // the core, not the whole rulebook
  }
  say('symlinked AGENTS.md and GEMINI.md for Codex and Gemini CLI',
    'Codex·Gemini CLI 용으로 AGENTS.md, GEMINI.md 심볼릭 링크를 만들었습니다');
}

if (previous && previous !== VERSION) {
  say(`updated: scripts/loop.mjs ${previous} → ${VERSION}`, `업데이트: scripts/loop.mjs ${previous} → ${VERSION}`);
  say('your edited rule files and .loop/ state are left alone (an untouched stock CLAUDE.md is replaced by the slim core) — delete a rule file and re-run to take the new edition',
    '수정한 규정 파일과 .loop/ 상태는 그대로 둡니다 (손대지 않은 원본 CLAUDE.md 는 핵심판으로 바뀜) — 새 규정을 받으려면 그 파일을 지우고 다시 실행하세요');
} else if (previous === VERSION) {
  say(`already current (${VERSION}), nothing changed`, `이미 최신입니다 (${VERSION}), 바뀐 것 없음`);
} else {
  say('installed scripts/loop.mjs', 'scripts/loop.mjs 를 설치했습니다');
}
if (placed.length) say(`added ${placed.join(', ')}`, `신규 ${placed.join(', ')}`);
else if (!previous) say('kept your existing rule files', '기존 규정 파일을 그대로 두었습니다');
if (slimmed) say('replaced the old CLAUDE.md that loaded all of LOOP.md every session with the core edition; LOOP.md is now read by section',
  'LOOP.md 전체를 매 세션 불러오던 옛 CLAUDE.md 를 핵심판으로 바꿨습니다 — 이제 LOOP.md 는 필요한 절만 읽습니다');
if (importKept) say('your CLAUDE.md is edited and still imports all of LOOP.md every session; to cut that, replace the @LOOP.md line with the core from the template',
  '수정된 CLAUDE.md 가 아직 LOOP.md 전체를 매 세션 불러옵니다 — 줄이려면 @LOOP.md 줄을 템플릿의 핵심판으로 바꾸세요');
if (migrated) say(`moved your CLAUDE.md to ${migrated}, read back for heavy items (LOOP.md section 5)`,
  `기존 CLAUDE.md 를 ${migrated} 로 옮겼습니다 — 중량 항목에서 다시 읽습니다 (LOOP.md 5절)`);

const name = path.basename(ROOT);
execSync(`node scripts/loop.mjs init --project ${JSON.stringify(name)} --lang ${LANG} --cursor --quiet`, { cwd: ROOT, stdio: 'inherit' });

// 삼킨 커밋 실패는 성공과 똑같아 보인다. 커밋했는지, 커밋할 게 없었는지, 실패했는지를 구분해 말한다.
// A swallowed commit failure looks exactly like a success: say which of the three happened.
let commit = 'none';
try {
  execSync('git add -A', { cwd: ROOT, stdio: 'ignore' });
  if (execSync('git status --porcelain', { cwd: ROOT, encoding: 'utf8' }).trim()) {
    execSync(`git commit -qm "v${VERSION}: install DOMANGCHA project loop"`, { cwd: ROOT, stdio: 'pipe' });
    commit = 'made';
  }
} catch (e) {
  // git's own stderr says why far better than "Command failed" does.
  const reason = String(e.stderr || '').trim() || String(e.message || e);
  commit = reason.split('\n').filter(Boolean)[0] || 'unknown error';
}

console.log('');
say(`installed · project ${name}`, `설치 완료 · 프로젝트 ${name}`);
if (commit === 'made') say(`committed as v${VERSION}`, `v${VERSION} 로 커밋했습니다`);
else if (commit !== 'none') {
  say(`the files are in place, but the commit did not run: ${commit}`,
    `파일은 제자리에 있지만 커밋은 실행되지 않았습니다: ${commit}`);
  say('commit them yourself when you are ready: git add -A && git commit',
    '준비되면 직접 커밋하세요: git add -A && git commit');
}
say('next: open Claude Code and just say what you want in plain language, no slash command needed',
  '다음 단계: Claude Code 를 열고 하고 싶은 일을 자연어로 그냥 말하면 됩니다 (슬래시 커맨드 불필요)');
say('start a bigger request with /ceo to raise it to the harness, which offers to install itself when needed',
  '더 큰 작업은 /ceo 로 시작하면 하네스로 올라갑니다 (필요할 때 설치를 제안합니다)');
console.log('');
