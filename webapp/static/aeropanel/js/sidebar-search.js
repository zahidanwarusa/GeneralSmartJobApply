$(document).ready(function () {
  // Sidebar search functionality
  $('#sidebarSearchInput').on('input', function () {
    const query = $(this).val().toLowerCase().trim();
    const sidebarNav = $('.sidebar-wrapper-nav');

    // Get all navigation items (both main items and submenu items)
    const allNavItems = sidebarNav.find('li').not('.nav-header');
    const navHeaders = sidebarNav.find('.nav-header');

    if (query === '') {
      // Show all items when search is empty
      allNavItems.show();
      navHeaders.show();
      $('.has-submenu .submenu').hide(); // Close all submenus
      return;
    }

    // Hide all items initially
    allNavItems.hide();
    navHeaders.hide();

    // Search through all navigation links
    allNavItems.each(function () {
      const $item = $(this);
      const $link = $item.find('.sidebar-nav-link').first();
      const linkText = $link.text().toLowerCase();

      // Check if the link text matches the query
      if (linkText.includes(query)) {
        $item.show();

        // If this is a submenu item, show its parent
        if ($item.closest('.submenu').length > 0) {
          $item.closest('.has-submenu').show();
          $item.closest('.submenu').show();
        }

        // If this has a submenu, expand it
        if ($item.hasClass('has-submenu')) {
          $item.find('.submenu').show();
        }
      }
    });

    // Show headers if any item in that section is visible
    navHeaders.each(function () {
      const $header = $(this);
      const $nextItems = $header.nextUntil('.nav-header');
      const hasVisibleItems = $nextItems.filter(':visible').length > 0;

      if (hasVisibleItems) {
        $header.show();
      }
    });
  });

  // Clear search on Escape key
  $('#sidebarSearchInput').on('keydown', function (e) {
    if (e.key === 'Escape') {
      $(this).val('').trigger('input');
    }
  });
});
