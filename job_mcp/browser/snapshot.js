// Runs inside each frame. Tags interactive elements with data-jm-ref and describes them.
// Arg: {prefix, max, includeLinks}. Returns an array of element descriptions.
({ prefix, max, includeLinks }) => {
  document.querySelectorAll('[data-jm-ref]').forEach(el => el.removeAttribute('data-jm-ref'));
  const SEL = 'input:not([type=hidden]), select, textarea, button, a[href], [role=button], [role=combobox], '
    + '[role=checkbox], [role=radio], [role=switch], [role=option], [contenteditable="true"]';
  const clean = s => (s || '').replace(/\s+/g, ' ').trim().slice(0, 160);
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const labelOf = el => {
    if (el.labels && el.labels.length) return clean([...el.labels].map(l => l.innerText).join(' '));
    const aria = el.getAttribute('aria-label');
    if (aria) return clean(aria);
    const by = el.getAttribute('aria-labelledby');
    if (by) return clean(by.split(/\s+/).map(id => document.getElementById(id)?.innerText || '').join(' '));
    if (el.placeholder) return clean(el.placeholder);
    // Many ATS forms put the question in a wrapper div rather than a <label>.
    let p = el.parentElement;
    for (let i = 0; i < 4 && p; i++, p = p.parentElement) {
      const t = clean(p.innerText);
      if (t && t.length < 160) return t;
    }
    return '';
  };
  // The question or section a control belongs to ("Resume/CV" vs "Cover Letter" for two "Attach" buttons).
  const groupOf = (el, own) => {
    let p = el.parentElement;
    for (let i = 0; i < 7 && p; i++, p = p.parentElement) {
      for (const head of p.querySelectorAll('label, legend, h2, h3, h4, [class*="label" i], [id$="label" i]')) {
        // A <label for=...> captions one specific sibling control, not the question as a whole.
        if (head.contains(el) || (head.tagName === 'LABEL' && head.htmlFor)) continue;
        const t = clean(head.innerText);
        // Skip the control's own caption ("Attach") and keep climbing to the question it belongs to.
        if (t && t !== own && t.length < 120) return t;
      }
    }
    return '';
  };
  const fillable = form => form ? form.querySelectorAll(
    'input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea').length : 0;

  const out = [];
  let n = 0;
  for (const el of document.querySelectorAll(SEL)) {
    if (out.length >= max) break;
    const tag = el.tagName.toLowerCase();
    const type = (el.getAttribute('type') || '').toLowerCase();
    const role = el.getAttribute('role') || '';
    // File inputs are usually hidden behind a styled button but still accept uploads.
    if (type !== 'file' && !visible(el)) continue;
    const text = clean(el.innerText || el.value);
    if (tag === 'a' && !includeLinks && !/apply|next|continue|review|sign in|log ?in/i.test(text)) continue;
    const ref = prefix + (n++);
    el.setAttribute('data-jm-ref', ref);
    const form = el.closest('form');
    const item = {
      ref, tag, type, role, label: labelOf(el), name: el.getAttribute('name') || '',
      required: !!(el.required || el.getAttribute('aria-required') === 'true'),
      in_form: !!form, form_fields: fillable(form),
      aria_autocomplete: el.getAttribute('aria-autocomplete') || '',
    };
    if (el.id) item.id = el.id.slice(0, 60);
    const group = groupOf(el, item.label || text);
    if (group && group !== item.label) item.group = group;
    if (['button', 'a'].includes(tag) || ['button', 'option'].includes(role) || ['submit', 'button'].includes(type)) item.text = text;
    if (tag === 'a') item.href = el.href.slice(0, 240);
    if (tag === 'select') {
      item.value = clean(el.selectedOptions[0]?.text);
      item.options = [...el.options].slice(0, 60).map(o => clean(o.text));
    } else if (type === 'checkbox' || type === 'radio' || ['checkbox', 'radio', 'switch'].includes(role)) {
      item.checked = el.checked ?? el.getAttribute('aria-checked') === 'true';
    } else if (type === 'password') {
      item.value = el.value ? '(set)' : '';
    } else if (type === 'file') {
      item.value = [...(el.files || [])].map(f => f.name).join(', ');
      item.accept = el.getAttribute('accept') || '';
    } else if (tag === 'input' || tag === 'textarea') {
      item.value = clean(el.value);
    }
    out.push(item);
  }
  return out;
}
