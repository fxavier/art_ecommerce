var updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var produtoId = this.dataset.produto;
    var action = this.dataset.action;
    console.log("USER:", user);
    if (user === "AnonymousUser") {
      addCookieItem(produtoId, action);
      console.log("Adding cookie");
    } else {
      updatePedidoUser(produtoId, action);
    }
  });
}

function updatePedidoUser(produtoId, action) {
  console.log("User is logged in, sending data..");

  var url = "/update-item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ produtoId: produtoId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // console.log("Data:", data);
      location.reload();
    });
}

function addCookieItem(produtoId, action) {
  console.log("Not logged in ....");

  if (action == "add") {
    if (cart[produtoId] == undefined) {
      cart[produtoId] = { quantidade: 1 };
    } else {
      cart[produtoId]["quantidade"] += 1;
    }
  }
  if (action == "remove") {
    cart[produtoId]["quantidade"] -= 1;

    if (cart[produtoId]["quantidade"] <= 0) {
      console.log("Item should be deleted");
      delete cart[produtoId];
    }
  }
  console.log("Cart:", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}
