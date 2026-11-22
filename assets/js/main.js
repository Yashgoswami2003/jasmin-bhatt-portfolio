document.addEventListener('DOMContentLoaded', () => {
  initMobileNavigation();
  initContactEnquiryForm();
  initEscapeKeyClose();
  initScrollProgress();
  initGalleryFilters();
});

function initMobileNavigation() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (!menuBtn || !mobileMenu) return;

  const setMenuState = (open, restoreFocus = false) => {
    mobileMenu.classList.toggle('hidden', !open);
    mobileMenu.dataset.open = open ? 'true' : 'false';
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close Navigation Menu' : 'Open Navigation Menu');
    menuBtn.textContent = open ? '✕' : '☰';

    if (!open && restoreFocus) {
      menuBtn.focus();
    }
  };

  menuBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
    setMenuState(!isExpanded, false);
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setMenuState(false, false));
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Node)) return;
    if (!mobileMenu.classList.contains('hidden') && !mobileMenu.contains(target) && !menuBtn.contains(target)) {
      setMenuState(false, false);
    }
  });

  window.addEventListener(
    'resize',
    () => {
      if (window.innerWidth >= 768 && !mobileMenu.classList.contains('hidden')) {
        setMenuState(false, false);
      }
    },
    { passive: true }
  );

  window.__closeMobileMenu = (restoreFocus = true) => setMenuState(false, restoreFocus);
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
    statusBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
}

function initEscapeKeyClose() {
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu && !mobileMenu.classList.contains('hidden')) {
      if (typeof window.__closeMobileMenu === 'function') {
        window.__closeMobileMenu(true);
      } else {
        mobileMenu.classList.add('hidden');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.textContent = '☰';
        menuBtn.focus();
      }
    }
  });
}

function initScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  if (!bar) return;

  let ticking = false;

  const updateProgress = () => {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
    bar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
    ticking = false;
  };

  const requestTick = () => {
    if (!ticking) {
      window.requestAnimationFrame(updateProgress);
      ticking = true;
    }
  };

  window.addEventListener('scroll', requestTick, { passive: true });
  window.addEventListener('resize', requestTick, { passive: true });
  updateProgress();
}

function initGalleryFilters() {
  const buttons = document.querySelectorAll('.filter-btn');
  const items = document.querySelectorAll('.gallery-item');
  if (!buttons.length || !items.length) return;

  buttons.forEach((btn) => {
    btn.setAttribute('aria-pressed', String(btn.classList.contains('active')));
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');
      buttons.forEach((b) => {
        b.classList.remove('active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');

      items.forEach((item) => {
        const cat = item.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    });
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