/* おちあい整骨院 共通JS */
(function () {
  // Hamburger menu
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.global-nav');
  const backdrop = document.querySelector('.nav-backdrop');

  if (hamburger && nav) {
    hamburger.addEventListener('click', toggle);
    backdrop && backdrop.addEventListener('click', close);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  function toggle() {
    const open = hamburger.getAttribute('aria-expanded') === 'true';
    open ? close() : open_nav();
  }
  function open_nav() {
    hamburger.setAttribute('aria-expanded', 'true');
    nav.classList.add('open');
    backdrop && backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    hamburger && hamburger.setAttribute('aria-expanded', 'false');
    nav && nav.classList.remove('open');
    backdrop && backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Scroll reveal
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.1 });
    reveals.forEach(el => io.observe(el));
  }
})();
