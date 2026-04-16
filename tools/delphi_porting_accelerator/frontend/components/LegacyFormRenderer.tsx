import React from 'react';

export interface LegacyNode {
  name: string;
  className: string;
  visualType: string;
  renderType?: string;
  caption?: string;
  text?: string;
  left: number;
  top: number;
  width: number;
  height: number;
  align?: string;
  color?: string;
  fontName?: string;
  fontHeight?: number;
  fontColor?: string;
  supported: boolean;
  tabStop?: boolean;
  tabOrder?: number | null;
  checked?: boolean | null;
  readOnly?: boolean | null;
  radioItems?: string[];
  radioColumns?: number | null;
  statusPanels?: Array<{ Text?: string; Width?: number; Alignment?: string }>;
  varGridRowCount?: number | null;
  gridColumns?: Array<{ caption?: string; field?: string; width?: number }>;
  events?: Record<string, string>;
  bindings?: Record<string, unknown>;
  children?: LegacyNode[];
}

function delphiEventDataAttrs(events: Record<string, string> | undefined): Record<string, string> {
  const out: Record<string, string> = {};
  if (!events) return out;
  for (const [k, v] of Object.entries(events)) {
    const short = k.startsWith('On') ? k.slice(2) : k;
    out[`data-delphi-event-${short.toLowerCase()}`] = String(v);
  }
  return out;
}

function delphiBindingDataAttrs(bindings: Record<string, unknown> | undefined): Record<string, string> {
  const out: Record<string, string> = {};
  if (!bindings) return out;
  for (const [k, v] of Object.entries(bindings)) {
    if (typeof v === 'string' || typeof v === 'number' || typeof v === 'boolean') {
      out[`data-delphi-binding-${k.toLowerCase()}`] = String(v);
    }
  }
  return out;
}

function nodeStyle(node: LegacyNode, root = false): React.CSSProperties {
  if (root) {
    return {
      position: 'relative',
      width: node.width,
      height: node.height,
      background: node.color || '#ececec',
    };
  }

  const base: React.CSSProperties = {
    position: 'absolute',
    boxSizing: 'border-box',
    left: node.left,
    top: node.top,
    width: node.width,
    height: node.height,
    color: node.fontColor || '#111827',
    fontFamily: node.fontName || 'Arial, sans-serif',
    fontSize: Math.max(10, Math.abs(node.fontHeight || 12)),
    background: node.color || undefined,
  };

  if (node.align === 'alClient') {
    return { ...base, left: 1, top: 1, right: 1, bottom: 1, width: 'auto', height: 'auto' };
  }
  if (node.align === 'alTop') {
    return { ...base, left: 0, top: 0, right: 0, width: 'auto' };
  }
  if (node.align === 'alBottom') {
    return { ...base, left: 0, bottom: 0, right: 0, top: 'auto', width: 'auto' };
  }
  if (node.align === 'alLeft') {
    return { ...base, left: 0, top: 0, bottom: 0, height: 'auto' };
  }
  if (node.align === 'alRight') {
    return { ...base, right: 0, top: 0, bottom: 0, left: 'auto', height: 'auto' };
  }

  return base;
}

function tabindexProps(node: LegacyNode): { tabIndex?: number } {
  if (node.tabOrder === undefined || node.tabOrder === null) return {};
  if (node.tabStop === false) return { tabIndex: -1 };
  return { tabIndex: node.tabOrder as number };
}

function renderGrid(node: LegacyNode) {
  const columns = node.gridColumns?.length
    ? node.gridColumns
    : [
        { caption: 'Column 1', field: 'col1' },
        { caption: 'Column 2', field: 'col2' },
      ];
  const rowCount = Math.max(1, node.varGridRowCount ?? 1);

  const rows = [];
  for (let r = 0; r < rowCount; r += 1) {
    rows.push(
      <tr key={`${node.name}-r${r}`}>
        {columns.map((column) => (
          <td key={`${node.name}-r${r}-${column.field}`}>&nbsp;</td>
        ))}
      </tr>,
    );
  }

  return (
    <table className="legacy-grid" style={{ width: '100%', height: '100%' }} role="grid">
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={`${node.name}-${column.field}`} style={{ width: column.width ? `${column.width}px` : undefined }}>
              {column.caption || column.field}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

function renderStatusBar(node: LegacyNode) {
  const panels = node.statusPanels || [];
  if (!panels.length) return null;
  return (
    <div
      className="legacy-statusbar-inner"
      style={{ display: 'flex', alignItems: 'stretch', width: '100%', fontSize: 11 }}
    >
      {panels.map((p, i) => (
        <span
          key={`${node.name}-sp${i}`}
          className="legacy-status-cell"
          style={{
            flex: `0 0 ${Math.max(24, p.Width ?? 60)}px`,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            borderRight: '1px solid #bfc5cc',
            padding: '0 4px',
          }}
        >
          {p.Text || ''}
        </span>
      ))}
    </div>
  );
}

function renderRadioGroup(node: LegacyNode) {
  const items = node.radioItems || [];
  const cols = Math.max(1, node.radioColumns ?? 1);
  if (!items.length) {
    return <div className="legacy-radiogroup-empty">(항목 없음)</div>;
  }
  const dis = node.enabled === false;
  return (
    <div
      className="legacy-radiogroup-grid"
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`,
        gap: '6px 12px',
      }}
    >
      {items.map((item, idx) => {
        const rid = `${node.name}_opt${idx}`;
        return (
          <label key={rid} className="legacy-radio-option" htmlFor={rid}>
            <input type="radio" name={node.name} id={rid} value={idx} disabled={dis} defaultChecked={idx === 0} />
            <span>{item}</span>
          </label>
        );
      })}
    </div>
  );
}

function LegacyNodeView({ node }: { node: LegacyNode }) {
  const renderType = node.renderType || node.visualType;
  const className = `legacy-node ${node.visualType} ${renderType} ${node.supported ? '' : 'unsupported'}`;
  const caption = node.caption || '';
  const dataAttrs = { ...delphiEventDataAttrs(node.events), ...delphiBindingDataAttrs(node.bindings) };

  const common = (
    <div
      className={className}
      style={nodeStyle(node)}
      data-delphi-class={node.className}
      data-delphi-render={renderType}
      {...dataAttrs}
    >
      {renderType === 'grid' ? renderGrid(node) : null}
      {renderType === 'progress' ? <progress max={100} value={25} style={{ width: '100%', height: '80%' }} /> : null}
      {renderType === 'statusbar' ? renderStatusBar(node) : null}
      {renderType === 'radiogroup' ? (
        <fieldset className="legacy-radiogroup-fieldset" style={{ border: '1px solid #bfc5cc', margin: 0, height: '100%' }}>
          <legend style={{ fontSize: 12 }}>{caption || node.name}</legend>
          {renderRadioGroup(node)}
        </fieldset>
      ) : null}
      {renderType === 'button' ? <button type="button">{caption || node.name}</button> : null}
      {renderType === 'label' ? <span className="legacy-label-text">{caption}</span> : null}
      {renderType === 'panel' && caption ? <span className="legacy-panel-caption">{caption}</span> : null}
      {renderType === 'checkbox' ? (
        <label htmlFor={`${node.name}_cb`}>
          <input
            id={`${node.name}_cb`}
            type="checkbox"
            defaultChecked={node.checked ?? false}
            disabled={node.enabled === false}
            {...tabindexProps(node)}
          />{' '}
          {caption || node.name}
        </label>
      ) : null}
      {renderType === 'radio' ? (
        <label htmlFor={`${node.name}_rb`}>
          <input
            id={`${node.name}_rb`}
            type="radio"
            name={`delphi-radio-${node.name}`}
            defaultChecked={false}
            disabled={node.enabled === false}
            {...tabindexProps(node)}
          />{' '}
          {caption || node.name}
        </label>
      ) : null}
      {(renderType === 'input' || renderType === 'number' || renderType === 'date') && !node.children?.length ? (
        <input
          type={renderType === 'number' ? 'number' : renderType === 'date' ? 'date' : 'text'}
          defaultValue={node.text || node.caption || ''}
          readOnly={node.readOnly === true}
          disabled={node.enabled === false}
          style={{ width: '100%', height: '100%', boxSizing: 'border-box' }}
          {...tabindexProps(node)}
        />
      ) : null}
      {renderType === 'textarea' && !node.children?.length ? (
        <textarea
          defaultValue={node.text || ''}
          readOnly={node.readOnly === true}
          disabled={node.enabled === false}
          style={{ width: '100%', height: '100%', boxSizing: 'border-box' }}
          {...tabindexProps(node)}
        />
      ) : null}
      {node.visualType === 'unsupported' ? (
        <span className="legacy-unsupported-badge">
          {node.className} → {renderType}
        </span>
      ) : null}
      {node.children?.map((child) => (
        <LegacyNodeView key={`${node.name}-${child.name}`} node={child} />
      ))}
    </div>
  );

  return common;
}

export function LegacyFormRenderer({ form }: { form: LegacyNode }) {
  return (
    <div className="legacy-wrapper card">
      <h2 className="section-title">{form.caption || form.name}</h2>
      <p className="small-muted">DFM에서 정규화한 기본 틀 미리보기</p>
      <div className="legacy-form" style={nodeStyle(form, true)}>
        {form.children?.map((child) => (
          <LegacyNodeView key={child.name} node={child} />
        ))}
      </div>
    </div>
  );
}
