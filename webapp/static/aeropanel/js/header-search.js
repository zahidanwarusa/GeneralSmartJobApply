
  $(document).ready(function () {
    // Sidebar navigation items for search
    const sidebarItems = [
      { title: 'Overview', url: '/dashboard/user', icon: 'bx-home' },
      { title: 'My Resumes', url: '/dashboard/user/resumes', icon: 'bx-file' },
      { title: 'Resume Builder', url: '/dashboard/user/resume-builder', icon: 'bx-edit' },
      { title: 'All Applications', url: '/dashboard/user/applications', icon: 'bx-briefcase' },
      { title: 'Kanban Board', url: '/dashboard/user/applications/kanban', icon: 'bx-grid-alt' },
      { title: 'Job Descriptions', url: '/dashboard/user/jobs', icon: 'bx-search-alt' },
      { title: 'Analytics', url: '/dashboard/user/analytics', icon: 'bx-chart-spline' },
      { title: 'Profile', url: '/dashboard/user/profile', icon: 'bx-user-circle' },
      { title: 'Settings', url: '/dashboard/user/settings', icon: 'bx-cog' },
      { title: 'Upgrade', url: '/dashboard/pricing', icon: 'bx-price-tag' },
    ];

    const trendingKeywords = [
      'Overview', 'Resumes', 'Applications', 'Jobs', 'Analytics',
      'Profile', 'Settings', 'Kanban', 'Upgrade'
    ];

    // Render trending keywords
    trendingKeywords.forEach(keyword => {
      $('#trendingKeywords').append(`
        <button class="keywords">
          <span><i class="bx bx-search fs-5"></i></span>
          <span>${keyword}</span>
        </button>
      `);
    });

    // Render initial popular items
    renderResults(sidebarItems);

    // Keyword click autofill
    $(document).on('click', '.keywords', function () {
      const text = $(this).text().trim();
      $('#searchInput').val(text).trigger('input');
    });

    // Simple sidebar search
    $('#searchInput').on('input', function () {
      const query = $(this).val().toLowerCase().trim();
      const resultsTitle = $('#resultsTitle');
      const resultsContainer = $('#searchResults');

      if (query === '') {
        resultsTitle.text('All Navigation');
        renderResults(sidebarItems);
        $('.trending-search').show();
        return;
      }

      // Filter sidebar items by title
      const filtered = sidebarItems.filter(item =>
        item.title.toLowerCase().includes(query)
      );

      resultsTitle.text('Search Results');
      $('.trending-search').hide();

      if (filtered.length > 0) {
        renderResults(filtered);
      } else {
        resultsContainer.html(`
          <div class="col">
            <div class="text-center p-4 text-muted">
              <i class="bx bx-search-alt fs-1 mb-2 d-block"></i>
              <p class="mb-0">No matching tabs found</p>
            </div>
          </div>
        `);
      }
    });

    // ✅ Auto-focus input when offcanvas opens
    const offcanvasEl = document.getElementById('offcanvasSearch');
    offcanvasEl.addEventListener('shown.bs.offcanvas', function () {
      $('#searchInput').trigger('focus');
    });

    // Helper function to render sidebar navigation cards
    function renderResults(items) {
      const container = $('#searchResults');
      container.empty();
      items.forEach(item => {
        container.append(`
          <div class="col">
            <a href="${item.url}" class="text-decoration-none">
              <div class="list-search-item d-flex align-items-center gap-3 p-3 border rounded-3 h-100">
                <div class="list-search-img d-flex align-items-center justify-content-center" style="min-width: 50px;">
                  <i class="bx ${item.icon} fs-1 text-primary"></i>
                </div>
                <div class="flex-grow-1">
                  <h5 class="mb-0 list-search-item-title text-dark">${item.title}</h5>
                </div>
                <div>
                  <i class="bx bx-chevron-right fs-5 text-muted"></i>
                </div>
              </div>
            </a>
          </div>
        `);
      });
    }
  });
