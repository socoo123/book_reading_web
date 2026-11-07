(() => {
  document.addEventListener('DOMContentLoaded', () => {
    const toc = document.querySelector('.toc');
    const links = [...document.querySelectorAll('.toc a[href^="#"]')];
    const sections = links
      .map((link) => document.getElementById(decodeURIComponent(link.hash.slice(1))))
      .filter(Boolean);

    const header = document.querySelector('.site-header');
    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.setAttribute('aria-hidden', 'true');
    progress.append(document.createElement('span'));
    header?.append(progress);

    let current = null;
    let queued = false;

    const highlight = (atEnd) => {
      if (!sections.length) return;
      const line = Math.min(160, window.innerHeight * 0.3);
      let active = sections[0];
      for (const section of sections) {
        if (section.getBoundingClientRect().top <= line) active = section;
        else break;
      }
      const last = sections[sections.length - 1];
      if (atEnd && last.getBoundingClientRect().top < window.innerHeight) active = last;
      if (active === current) return;
      current = active;
      for (const link of links) {
        if (link.hash.slice(1) === active.id) {
          link.setAttribute('aria-current', 'location');
          if (toc && toc.scrollHeight > toc.clientHeight) {
            const top = link.offsetTop - toc.clientHeight / 2;
            toc.scrollTo({ top: Math.max(0, top) });
          }
        } else {
          link.removeAttribute('aria-current');
        }
      }
    };

    const update = () => {
      queued = false;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 1;
      progress.firstChild.style.transform = `scaleX(${ratio})`;
      highlight(max > 0 && window.scrollY >= max - 2);
    };

    const schedule = () => {
      if (!queued) {
        queued = true;
        requestAnimationFrame(update);
      }
    };

    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    update();
  });
})();
