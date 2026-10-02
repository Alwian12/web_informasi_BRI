document.addEventListener('DOMContentLoaded', function() {
  const showPassword = document.getElementById('showPassword');
  const passwordInput = document.getElementById('passwordInput');

  if (showPassword && passwordInput) {
    showPassword.addEventListener('change', function() {
      passwordInput.type = this.checked ? 'text' : 'password';
    });
  }

  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('open');
    });

    sidebar.querySelectorAll('.nav-link').forEach(function(link) {
      link.addEventListener('click', function() {
        sidebar.classList.remove('open');
      });
    });
  }

  const adminSearch = document.getElementById('adminSearch');
  if (adminSearch) {
    adminSearch.addEventListener('input', function() {
      const query = this.value.trim().toLowerCase();
      document.querySelectorAll('.admin-body table tbody tr').forEach(function(row) {
        row.hidden = Boolean(query) && !row.textContent.toLowerCase().includes(query);
      });
      document.querySelectorAll('.admin-body .activity-list li').forEach(function(item) {
        item.hidden = Boolean(query) && !item.textContent.toLowerCase().includes(query);
      });
    });
  }

  document.querySelectorAll('.reply-textarea').forEach(function(textarea) {
    const counter = document.getElementById(textarea.id.replace('reply', 'replyCount'));
    if (counter) {
      textarea.addEventListener('input', function() {
        counter.textContent = this.value.length;
      });
    }
  });

  const navbar = document.querySelector('.site-navbar');
  if (navbar) {
    const applyNavbarState = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 16);
    };
    applyNavbarState();
    window.addEventListener('scroll', applyNavbarState, { passive: true });
  }

  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealItems.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('visible'));
  }

  const scrollButton = document.createElement('button');
  scrollButton.className = 'btn btn-primary scroll-top';
  scrollButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
  document.body.appendChild(scrollButton);

  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      scrollButton.classList.add('show');
    } else {
      scrollButton.classList.remove('show');
    }
  });

  scrollButton.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
