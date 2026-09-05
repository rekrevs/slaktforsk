'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

type View = 'overview' | 'tree' | 'people';
type PersonState = 'documented' | 'open' | 'conflict' | 'lead';
type Claim = {
  id: string;
  statement: string;
  status: string;
  reliability: string;
  citations: string[];
};
type Relation = { target: string; relation: string; status: string };
type Person = {
  id: string;
  name: string;
  identity: string;
  researchStatus: string;
  state: PersonState;
  lifespan: string;
  private: boolean;
  claims: Claim[];
  relations: Relation[];
  branches: string[];
  depths: Record<string, number>;
};
type LogEntry = { date: string; batch: number; title: string; summary: string };
type DashboardData = {
  generatedAt: string;
  activeWork: {
    id: string;
    status: string;
    phase: string;
    summary: string;
    latest: LogEntry | null;
  } | null;
  stats: {
    people: number;
    assertions: number;
    sources: number;
    citations: number;
    media: number;
    assertionStatuses: Record<string, number>;
  };
  progress: Array<{
    id: string;
    label: string;
    knownAncestors: number;
    generations: Array<{ depth: number; known: number; possible: number }>;
  }>;
  people: Person[];
  parentEdges: Array<{ child: string; parent: string; relation: string }>;
  recentChanges: LogEntry[];
};

const DashboardContext = createContext<DashboardData | null>(null);

function useDashboardData() {
  const value = useContext(DashboardContext);
  if (!value) throw new Error('Dashboarddata saknas');
  return value;
}
const stateLabels: Record<PersonState, string> = {
  documented: 'Väl belagd',
  open: 'Öppen fråga',
  conflict: 'Källkonflikt',
  lead: 'Påbörjad',
};

function formatDate(value: string) {
  return new Intl.DateTimeFormat('sv-SE', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${value}T12:00:00`));
}

function shortName(name: string, limit = 28) {
  return name.length > limit ? `${name.slice(0, limit - 1)}…` : name;
}

function splitName(name: string) {
  if (name.length <= 25) return [name];
  const words = name.split(' ');
  let first = '';
  while (words.length && `${first} ${words[0]}`.trim().length <= 24) {
    first = `${first} ${words.shift()}`.trim();
  }
  return [first, words.join(' ') || ''];
}

function PersonPanel({
  person,
  peopleById,
  onSelect,
  onClose,
}: {
  person: Person;
  peopleById: Map<string, Person>;
  onSelect: (id: string) => void;
  onClose?: () => void;
}) {
  const [showEvidence, setShowEvidence] = useState(false);
  const statusText = person.researchStatus || person.identity || 'Personakten är registrerad men saknar ännu en sammanfattande forskningsstatus.';

  return (
    <aside className="person-panel" aria-label={`Personkort för ${person.name}`}>
      <div className="panel-topline">
        <span className={`state-dot ${person.state}`} />
        <span>{stateLabels[person.state]}</span>
        {onClose && <button className="icon-button" onClick={onClose} aria-label="Stäng personkort">×</button>}
      </div>
      <p className="person-id">{person.id}</p>
      <h3>{person.name}</h3>
      <p className="lifespan">{person.lifespan}</p>
      <p className="person-story">{person.private ? 'Nutida familjemedlem. Känsliga detaljer hålls utanför översiktsvyn.' : statusText}</p>

      {person.relations.length > 0 && (
        <div className="panel-section">
          <h4>Närmaste familj</h4>
          <div className="relation-list">
            {person.relations.slice(0, 10).map((relation) => {
              const relative = peopleById.get(relation.target);
              return relative ? (
                <button key={`${relation.target}-${relation.relation}`} onClick={() => onSelect(relation.target)}>
                  <span>{relation.relation}</span>
                  <strong>{relative.name}</strong>
                </button>
              ) : null;
            })}
          </div>
        </div>
      )}

      {!person.private && person.claims.length > 0 && (
        <div className="panel-section evidence-section">
          <button className="evidence-toggle" onClick={() => setShowEvidence((value) => !value)} aria-expanded={showEvidence}>
            {showEvidence ? 'Dölj beläggen' : `Visa beläggen (${person.claims.length})`}
            <span>{showEvidence ? '−' : '+'}</span>
          </button>
          {showEvidence && (
            <div className="claim-list">
              {person.claims.slice(0, 8).map((claim) => (
                <article key={claim.id}>
                  <span className={`claim-status ${claim.status.toLowerCase()}`}>{claim.status || 'BEDÖMS'}</span>
                  <p>{claim.statement}</p>
                  <small>{claim.citations.join(', ') || 'Belägg registreras'}</small>
                </article>
              ))}
              {person.claims.length > 8 && <p className="more-note">Ytterligare {person.claims.length - 8} påståenden finns i personakten.</p>}
            </div>
          )}
        </div>
      )}
    </aside>
  );
}

type TreeNode = { id: string; depth: number; slot: number; x: number; y: number };
type TreeLine = { from: TreeNode; to: TreeNode };

function TreeView({ peopleById }: { peopleById: Map<string, Person> }) {
  const data = useDashboardData();
  const [root, setRoot] = useState('P-0004');
  const [maxDepth, setMaxDepth] = useState(4);
  const [zoom, setZoom] = useState(0.82);
  const [selectedId, setSelectedId] = useState('P-0004');
  const [panelOpen, setPanelOpen] = useState(true);

  const tree = useMemo(() => {
    const nodeWidth = 208;
    const nodeHeight = 72;
    const levelGap = 252;
    const rowHeight = 92;
    const canvasHeight = Math.max(650, (2 ** maxDepth) * rowHeight);
    const nodes: TreeNode[] = [];
    const lines: TreeLine[] = [];
    let current = [{ id: root, depth: 0, slot: 0 }];

    for (let depth = 0; depth <= maxDepth; depth += 1) {
      const next: Array<{ id: string; depth: number; slot: number }> = [];
      for (const item of current) {
        const node = {
          ...item,
          x: 42 + item.depth * levelGap,
          y: ((item.slot + 0.5) * canvasHeight) / (2 ** item.depth) - nodeHeight / 2,
        };
        nodes.push(node);
        if (depth === maxDepth) continue;
        const parents = data.parentEdges
          .filter((edge) => edge.child === item.id)
          .sort((a, b) => {
            const order = (relation: string) => /far|fader/i.test(relation) ? 0 : /mor|moder/i.test(relation) ? 1 : 2;
            return order(a.relation) - order(b.relation);
          });
        parents.slice(0, 2).forEach((edge, index) => {
          const parentItem = { id: edge.parent, depth: depth + 1, slot: item.slot * 2 + index };
          const parentNode = {
            ...parentItem,
            x: 42 + parentItem.depth * levelGap,
            y: ((parentItem.slot + 0.5) * canvasHeight) / (2 ** parentItem.depth) - nodeHeight / 2,
          };
          lines.push({ from: node, to: parentNode });
          next.push(parentItem);
        });
      }
      current = next;
    }

    return { nodes, lines, width: 42 + maxDepth * levelGap + nodeWidth + 45, height: canvasHeight, nodeWidth, nodeHeight };
  }, [data.parentEdges, root, maxDepth]);

  const selected = peopleById.get(selectedId) ?? peopleById.get(root)!;

  function selectPerson(id: string) {
    setSelectedId(id);
    setPanelOpen(true);
  }

  return (
    <section className="workspace tree-workspace" aria-labelledby="tree-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Utforska sambanden</p>
          <h1 id="tree-title">Släktträdet</h1>
          <p>Följ en anlinje och öppna en person för att läsa den mänskliga berättelsen bakom noden.</p>
        </div>
        <div className="tree-legend" aria-label="Teckenförklaring">
          {Object.entries(stateLabels).map(([state, label]) => <span key={state}><i className={`state-dot ${state}`} />{label}</span>)}
        </div>
      </div>

      <div className="tree-toolbar">
        <label>Utgångsperson
          <select value={root} onChange={(event) => { setRoot(event.target.value); setSelectedId(event.target.value); }}>
            <option value="P-0004">Sverker Adam</option>
            <option value="P-0210">Kristina</option>
          </select>
        </label>
        <label>Generationer
          <select value={maxDepth} onChange={(event) => setMaxDepth(Number(event.target.value))}>
            {[2, 3, 4, 5].map((depth) => <option value={depth} key={depth}>{depth}</option>)}
          </select>
        </label>
        <div className="zoom-controls" aria-label="Zooma trädet">
          <button onClick={() => setZoom((value) => Math.max(0.45, value - 0.1))} aria-label="Zooma ut">−</button>
          <span>{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom((value) => Math.min(1.25, value + 0.1))} aria-label="Zooma in">+</button>
        </div>
        <p>Dra med rullisterna för att röra dig i trädet.</p>
      </div>

      <div className={`tree-layout ${panelOpen ? 'with-panel' : ''}`}>
        <div className="tree-viewport" tabIndex={0} aria-label="Rullbart släktträd">
          <svg
            className="tree-canvas"
            width={tree.width * zoom}
            height={tree.height * zoom}
            viewBox={`0 0 ${tree.width} ${tree.height}`}
            role="tree"
            aria-label={`Anor till ${peopleById.get(root)?.name}`}
          >
            <g className="tree-lines">
              {tree.lines.map((line, index) => {
                const fromX = line.from.x + tree.nodeWidth;
                const fromY = line.from.y + tree.nodeHeight / 2;
                const toX = line.to.x;
                const toY = line.to.y + tree.nodeHeight / 2;
                const middle = fromX + (toX - fromX) / 2;
                return <path key={index} d={`M ${fromX} ${fromY} C ${middle} ${fromY}, ${middle} ${toY}, ${toX} ${toY}`} />;
              })}
            </g>
            {tree.nodes.map((node) => {
              const person = peopleById.get(node.id);
              if (!person) return null;
              const lines = splitName(person.name);
              return (
                <g
                  className={`tree-node ${person.state} ${selectedId === person.id ? 'selected' : ''}`}
                  key={`${node.id}-${node.depth}-${node.slot}`}
                  role="treeitem"
                  tabIndex={0}
                  aria-label={`${person.name}, ${person.lifespan}, ${stateLabels[person.state]}`}
                  onClick={() => selectPerson(person.id)}
                  onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') selectPerson(person.id); }}
                >
                  <rect x={node.x} y={node.y} width={tree.nodeWidth} height={tree.nodeHeight} rx="3" />
                  <circle cx={node.x + 17} cy={node.y + 17} r="4" />
                  <text className="node-name" x={node.x + 30} y={node.y + 22}>{lines[0]}</text>
                  {lines[1] && <text className="node-name second" x={node.x + 30} y={node.y + 39}>{lines[1]}</text>}
                  <text className="node-years" x={node.x + 30} y={node.y + 58}>{person.lifespan}</text>
                  <text className="node-id" x={node.x + tree.nodeWidth - 12} y={node.y + 58}>{person.id}</text>
                </g>
              );
            })}
          </svg>
        </div>
        {panelOpen && selected && <PersonPanel key={selected.id} person={selected} peopleById={peopleById} onSelect={selectPerson} onClose={() => setPanelOpen(false)} />}
      </div>
    </section>
  );
}

function PeopleView({ peopleById }: { peopleById: Map<string, Person> }) {
  const data = useDashboardData();
  const [query, setQuery] = useState('');
  const [stateFilter, setStateFilter] = useState('all');
  const [branchFilter, setBranchFilter] = useState('all');
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase('sv-SE');
    return data.people
      .filter((person) => stateFilter === 'all' || person.state === stateFilter)
      .filter((person) => branchFilter === 'all' || person.branches.includes(branchFilter))
      .filter((person) => !normalized || `${person.name} ${person.identity} ${person.researchStatus}`.toLocaleLowerCase('sv-SE').includes(normalized))
      .sort((a, b) => a.name.localeCompare(b.name, 'sv'));
  }, [data.people, query, stateFilter, branchFilter]);

  const selected = selectedId ? peopleById.get(selectedId) : null;

  return (
    <section className="workspace people-workspace" aria-labelledby="people-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Hela kunskapen</p>
          <h1 id="people-title">Personer</h1>
          <p>Sök bland {data.stats.people} personakter. Källapparaten finns nära, men ligger undan tills du vill se den.</p>
        </div>
      </div>

      <div className="people-toolbar">
        <label className="search-field">
          <span>Sök person, plats eller år</span>
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Skriv exempelvis Fredberg eller Indal" />
        </label>
        <label>Status
          <select value={stateFilter} onChange={(event) => setStateFilter(event.target.value)}>
            <option value="all">Alla lägen</option>
            {Object.entries(stateLabels).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
          </select>
        </label>
        <label>Anlinje
          <select value={branchFilter} onChange={(event) => setBranchFilter(event.target.value)}>
            <option value="all">Hela trädet</option>
            <option value="P-0004">Sverker Adam</option>
            <option value="P-0210">Kristina</option>
          </select>
        </label>
      </div>

      <div className={`people-layout ${selected ? 'with-panel' : ''}`}>
        <div>
          <p className="result-count">{filtered.length} personer</p>
          <div className="people-list">
            {filtered.map((person) => (
              <button className="person-row" key={person.id} onClick={() => setSelectedId(person.id)}>
                <span className={`state-dot ${person.state}`} />
                <span className="person-row-name"><strong>{person.name}</strong><small>{person.id}</small></span>
                <span className="person-row-years">{person.lifespan}</span>
                <span className="person-row-summary">{person.private ? 'Nutida familjemedlem' : shortName(person.identity || person.researchStatus, 88)}</span>
                <span className="row-arrow">→</span>
              </button>
            ))}
          </div>
        </div>
        {selected && <PersonPanel key={selected.id} person={selected} peopleById={peopleById} onSelect={setSelectedId} onClose={() => setSelectedId(null)} />}
      </div>
    </section>
  );
}

function Overview({ go }: { go: (view: View) => void }) {
  const data = useDashboardData();
  const latest = data.activeWork?.latest ?? data.recentChanges[0] ?? null;
  const hasActiveWork = Boolean(data.activeWork);
  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">Levande familjehistoria</p>
          <h1>Vi följer människorna,<br />inte bara namnen.</h1>
          <p className="lede">En ren vy över hur trädet växer, vad källorna berättar och var nästa fråga väntar.</p>
        </div>
        <button className="hero-stamp" onClick={() => go('people')} aria-label={`Visa ${data.stats.people} personer`}>
          <span>{data.stats.people}</span>
          <small>personöden</small>
        </button>
      </section>

      <section className="overview">
        <div className="section-heading">
          <div><p className="eyebrow">Just nu</p><h2>{hasActiveWork ? 'Forskningen rör sig framåt' : 'Ingen aktiv uppgift'}</h2></div>
          <span className="status-pill">{hasActiveWork ? (data.activeWork?.phase === 'DOING' ? 'Pågår' : 'Aktiv') : 'Väntar'}</span>
        </div>

        <div className="focus-grid">
          <article className="focus-card">
            <div className="card-number">{data.activeWork?.id ?? '—'}</div>
            <p className="card-label">{hasActiveWork ? 'Aktiv forskningslinje' : 'Aktuellt projektläge'}</p>
            <h3>{data.activeWork?.summary ?? 'En tom uppgiftskö visar inte att forskningen är färdig. Projektets dokumenterade källäge avgör vad som återstår.'}</h3>
            {latest && <p className="latest-title">Senast: {latest.title}</p>}
            {latest && <p>{latest.summary}</p>}
            <a href="#recent">Se senaste fynden <span>→</span></a>
          </article>
          <div className="metric-grid" aria-label="Projektets omfattning">
            <article><strong>{data.stats.assertions.toLocaleString('sv-SE')}</strong><span>källbedömda<br />påståenden</span></article>
            <article><strong>{data.stats.citations}</strong><span>exakta<br />belägg</span></article>
            <article><strong>{data.stats.sources}</strong><span>undersökta<br />källor</span></article>
            <article><strong>{data.stats.media.toLocaleString('sv-SE')}</strong><span>bevarade<br />original</span></article>
          </div>
        </div>

        <div className="branch-grid">
          {data.progress.map((branch) => (
            <article className="branch-card" key={branch.id}>
              <div className="branch-top">
                <div><p className="card-label">Anlinje</p><h3>{branch.label}</h3></div>
                <strong>{branch.knownAncestors}</strong>
              </div>
              <div className="generation-bars">
                {branch.generations.slice(0, 5).map((generation) => (
                  <div className="generation" key={generation.depth}>
                    <span>Generation {generation.depth}</span>
                    <div className="bar"><i style={{ width: `${Math.min(100, generation.known / generation.possible * 100)}%` }} /></div>
                    <b>{generation.known}/{generation.possible}</b>
                  </div>
                ))}
              </div>
              <button className="text-link" onClick={() => go('tree')}>Öppna anlinjen <span>→</span></button>
            </article>
          ))}
        </div>
      </section>

      <section className="recent-section" id="recent">
        <div className="section-heading">
          <div><p className="eyebrow">Forskningsdagbok</p><h2>Senaste rörelserna i trädet</h2></div>
        </div>
        <div className="timeline">
          {data.recentChanges.slice(0, 6).map((entry, index) => (
            <article key={`${entry.date}-${entry.batch}`}>
              <div className="timeline-mark"><span>{entry.batch || index + 1}</span></div>
              <div>
                <time>{formatDate(entry.date)}</time>
                <h3>{entry.title}</h3>
                <p>{entry.summary}</p>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

function DashboardApp() {
  const data = useDashboardData();
  const [view, setView] = useState<View>(() => {
    if (typeof window === 'undefined') return 'overview';
    const requested = window.location.hash.slice(1) as View;
    return ['overview', 'tree', 'people'].includes(requested) ? requested : 'overview';
  });
  const peopleById = useMemo(() => new Map(data.people.map((person) => [person.id, person])), [data.people]);

  function go(next: View) {
    setView(next);
    window.history.replaceState(null, '', `#${next}`);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <main id="top">
      <header className="site-header">
        <button className="brand" onClick={() => go('overview')} aria-label="Till översikten">
          <span className="brand-mark">SJ</span>
          <span><strong>Släktarkivet</strong><small>Forskningsöversikt</small></span>
        </button>
        <nav aria-label="Huvudnavigering">
          {(['overview', 'tree', 'people'] as View[]).map((item) => (
            <button className={view === item ? 'active' : ''} key={item} onClick={() => go(item)} aria-current={view === item ? 'page' : undefined}>
              {{ overview: 'Översikt', tree: 'Träd', people: 'Personer' }[item]}
            </button>
          ))}
        </nav>
        <span className="freshness"><i /> Uppdaterad {data.activeWork?.latest?.date ?? 'idag'}</span>
      </header>

      {view === 'overview' && <Overview go={go} />}
      {view === 'tree' && <TreeView peopleById={peopleById} />}
      {view === 'people' && <PeopleView peopleById={peopleById} />}

      <footer>
        <strong>Släktarkivet</strong>
        <span>Härledd vy · forskningsfilerna är alltid originalet</span>
        <span>{data.stats.people} personer · {data.stats.citations} belägg</span>
      </footer>
    </main>
  );
}

export default function Home() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loadError, setLoadError] = useState(false);

  useEffect(() => {
    let active = true;
    fetch('/data/project.json')
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<DashboardData>;
      })
      .then((value) => { if (active) setDashboardData(value); })
      .catch(() => { if (active) setLoadError(true); });
    return () => { active = false; };
  }, []);

  if (!dashboardData) {
    return (
      <main className="loading-view" aria-live="polite">
        <span className="brand-mark">SJ</span>
        <p className="eyebrow">Släktarkivet</p>
        <h1>{loadError ? 'Kunde inte läsa projektets översikt.' : 'Samlar ihop släktträdet…'}</h1>
        {loadError && <p>Generera dashboardens data och ladda om sidan.</p>}
      </main>
    );
  }

  return <DashboardContext.Provider value={dashboardData}><DashboardApp /></DashboardContext.Provider>;
}
