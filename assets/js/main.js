document.addEventListener('DOMContentLoaded', () => {
  initMobileNavigation();
  initContactEnquiryForm();
  initEscapeKeyClose();
});

function initMobileNavigation() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (!menuBtn || !mobileMenu) return;

  const setMenuState = (open) => {
    mobileMenu.classList.toggle('hidden', !open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? '✕' : '☰';
  };

  menuBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
    setMenuState(!isExpanded);
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setMenuState(false));
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Node)) return;
    if (!mobileMenu.classList.contains('hidden') && !mobileMenu.contains(target) && !menuBtn.contains(target)) {
      setMenuState(false);
    }
  });
}

function initContactEnquiryForm() {
  const form = document.getElementById('demo-contact-form');
  if (!form) return;

  const purposeSelect = document.getElementById('enquiry-purpose');
  const orgLabel = document.getElementById('org-label');
  const orgInput = document.getElementById('org-input');
  const statusBox = document.getElementById('form-status');

  const purposeConfig = {
    'film-ott-audio': {
      label: 'Production House / OTT / Audio Platform',
      placeholder: 'e.g., Studio, OTT Platform, Audio Label'
    },
    'books-poetry-event': {
      label: 'Publisher / Literary or Cultural Event Organizer',
      placeholder: 'e.g., Book Fair, Literary Forum, Poetry Show'
    },
    'tax-legal-academic': {
      label: 'Institution / Business / Advisory Context',
      placeholder: 'e.g., College, University, Advisory Matter'
    },
    'media-press': {
      label: 'Publication / Media Channel',
      placeholder: 'e.g., Newspaper, Interview Desk, Digital Media'
    }
  };

  const syncPurposeFields = () => {
    if (!purposeSelect || !orgLabel || !orgInput) return;
    const selected = purposeConfig[purposeSelect.value] || purposeConfig['film-ott-audio'];
    orgLabel.textContent = selected.label;
    orgInput.placeholder = selected.placeholder;
  };

  if (purposeSelect) {
    purposeSelect.addEventListener('change', syncPurposeFields);
    syncPurposeFields();
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!statusBox) return;

    const formData = new FormData(form);
    const name = String(formData.get('name') || '').trim();
    const purposeText = purposeSelect
      ? purposeSelect.options[purposeSelect.selectedIndex]?.text || 'Enquiry'
      : 'Enquiry';

    statusBox.classList.remove('hidden');
    statusBox.innerHTML = `
      <strong class="font-semibold text-slate-950">Preview Captured${name ? ` for ${escapeHtml(name)}` : ''}:</strong>
      Your <span class="font-semibold">${escapeHtml(purposeText)}</span> note is ready for live endpoint routing once approved. No public database storage or sensitive script exposure is active.
    `;
  });
}

function initEscapeKeyClose() {
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu && !mobileMenu.classList.contains('hidden')) {
      mobileMenu.classList.add('hidden');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.textContent = '☰';
    }
  });
}

function escapeHtml(str) {
  return str
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}