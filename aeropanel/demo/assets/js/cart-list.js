// ...existing code...
$(function () {
  "use strict";

  const initialItems = [
    { title: "Project Manager Tee", img: "assets/images/products/01.png", color: "Silver", size: "Large", pricePerItem: 23, quantity: 2 },
    { title: "Cozy Pink Zip-Up Hoodie", img: "assets/images/products/02.png", color: "Silver", size: "Large", pricePerItem: 23, quantity: 2 },
    { title: "Adidas Running Shoes", img: "assets/images/products/03.png", color: "Black", size: "Medium", pricePerItem: 35, quantity: 1 },
    { title: "Elegant White Leather Handbag", img: "assets/images/products/04.png", color: "Gold", size: "Small", pricePerItem: 15, quantity: 3 },
    { title: "Classic Green Formal Shirt", img: "assets/images/products/05.png", color: "Blue", size: "Extra Large", pricePerItem: 14, quantity: 6 }
  ];

  var $container = $("#cartList");
  if (!$container.length) return;

  var $listEl = $("#cartItemsList");
  var $clearBtn = $("#cartClearBtn");
  var $summaryEl = $("#cartSummary");

  var items = initialItems.map(function (it) {
    return $.extend({}, it, { quantity: Math.max(1, Math.round(it.quantity || 1)) });
  });

  function formatPrice(v) {
    return v.toFixed(2) + " USD";
  }

  function calcSummary() {
    var total = items.reduce(function (acc, it) { return acc + it.pricePerItem * it.quantity; }, 0);
    var qty = items.reduce(function (acc, it) { return acc + it.quantity; }, 0);
    return { total: total, qty: qty };
  }

  function buildQtyOptions(currentQty) {
    var html = "";
    for (var i = 1; i <= 10; i++) {
      html += '<option value="' + i + '"' + (i === Number(currentQty) ? " selected" : "") + '>Qty: ' + i + '</option>';
    }
    return html;
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (s) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[s]);
    });
  }

  function render() {
    if (!items.length) {
      $listEl.html('<li class="list-group-item text-muted">Your cart is empty.</li>');
      $summaryEl.text("");
      return;
    }

    var html = "";
    $.each(items, function (idx, item) {
      html +=
        '<li class="list-group-item d-flex flex-column flex-md-row justify-content-between border-bottom py-3 gap-3" data-index="' + idx + '">' +
          '<div class="d-flex align-items-center gap-3">' +
            '<img src="' + escapeHtml(item.img) + '" alt="' + escapeHtml(item.title) + '" class="rounded-3 bg-light p-2" width="80" height="80" />' +
            '<div>' +
              '<h6 class="fw-semibold mb-0">' + escapeHtml(item.title) + '</h6>' +
              '<small class="text-muted d-block">Color: ' + escapeHtml(item.color) + '</small>' +
              '<small class="text-muted d-block">Size: ' + escapeHtml(item.size) + '</small>' +
              '<small class="text-muted d-block">Price: ' + item.pricePerItem + ' USD / per item</small>' +
            '</div>' +
          '</div>' +

          '<div class="d-flex align-items-center gap-3 mt-2 mt-md-0">' +
            '<div>' +
              '<select class="form-select form-select-sm cart-qty-select" data-index="' + idx + '">' + buildQtyOptions(item.quantity) + '</select>' +
            '</div>' +
            '<div class="fw-semibold item-total" data-index="' + idx + '">' + formatPrice(item.pricePerItem * item.quantity) + '</div>' +
            '<button class="btn btn-outline-primary p-0 wh-35 btn-fav" data-index="' + idx + '" title="Save for later">' +
              '<i class="bx bx-heart lh-0 fs-5"></i>' +
            '</button>' +
            '<button class="btn btn-outline-danger p-0 wh-35 btn-remove" data-index="' + idx + '" title="Remove">' +
              '<i class="bx bx-x lh-0 fs-5"></i>' +
            '</button>' +
          '</div>' +
        '</li>';
    });

    $listEl.html(html);
    var s = calcSummary();
    $summaryEl.text("Items: " + s.qty + " — Total: " + formatPrice(s.total));
  }

  // delegated handlers
  $listEl.on("change", ".cart-qty-select", function () {
    var $sel = $(this);
    var idx = Number($sel.data("index"));
    var qty = Math.max(1, parseInt($sel.val(), 10) || 1);
    if (items[idx]) {
      items[idx].quantity = qty;
      $listEl.find('.item-total[data-index="' + idx + '"]').text(formatPrice(items[idx].pricePerItem * qty));
      var s = calcSummary();
      $summaryEl.text("Items: " + s.qty + " — Total: " + formatPrice(s.total));
    }
  });

  $listEl.on("click", ".btn-remove", function (e) {
    e.preventDefault();
    var idx = Number($(this).data("index"));
    if (!isNaN(idx)) {
      items.splice(idx, 1);
      render();
    }
  });

  $listEl.on("click", ".btn-fav", function (e) {
    e.preventDefault();
    var $btn = $(this);
    $btn.toggleClass("active");
    $btn.find("i").toggleClass("text-danger");
  });

  $clearBtn.on("click", function (e) {
    e.preventDefault();
    items = [];
    render();
  });

  // initial render
  render();
});
// ...existing code...