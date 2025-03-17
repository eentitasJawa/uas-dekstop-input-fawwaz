const products = {
  'Si Putih': { name: 'Si Putih', price: 65000, image: 'Siputih.jpg' },
  'Sagaras': { name: 'Sagaras', price: 52000, image: 'Sagaras.jpg' }
};

let cart = {};  
let totalPrice = 0;  

// Fungsi untuk menampilkan daftar produk
function displayProducts() {
    const productList = document.getElementById("productList");
    productList.innerHTML = '';  

    for (const key in products) {
        const product = products[key];

        // Buat elemen untuk produk
        const productElement = document.createElement("div");
        productElement.classList.add("product-item");
        productElement.innerHTML = `
            <img src="${product.image}" alt="${product.name}" width="100">
            <h3>${product.name}</h3>
            <p>Rp ${product.price}</p>
        `;
        
        // Tambahkan event listener agar bisa diklik
        productElement.addEventListener("click", function() {
            addToCart(product.name);
        });

        // Masukkan ke dalam daftar produk
        productList.appendChild(productElement);
    }
}

// Fungsi untuk menambahkan produk ke dalam keranjang
function addToCart(bookTitle) {
    const formattedTitle = bookTitle.trim(); 

    if (products[formattedTitle]) {
        if (cart[formattedTitle]) {
            cart[formattedTitle].quantity += 1;
        } else {
            cart[formattedTitle] = {
                name: products[formattedTitle].name,
                price: products[formattedTitle].price,
                image: products[formattedTitle].image,
                quantity: 1
            };
        }
        updateCart();
    } else {
        alert("Judul buku tidak ditemukan!");
    }
}

// Fungsi untuk memperbarui tampilan keranjang
function updateCart() {
    const cartItems = document.getElementById("cartItems");
    cartItems.innerHTML = '';  
    totalPrice = 0;  

    for (const title in cart) {
        const item = cart[title];
        const subtotal = item.price * item.quantity;
        totalPrice += subtotal;

        cartItems.innerHTML += `
            <tr>
                <td><img src="${item.image}" alt="${item.name}" width="50"></td>
                <td>${item.name}</td>
                <td>Rp ${item.price}</td>
                <td>${item.quantity}</td>
                <td>Rp ${subtotal}</td>
            </tr>
        `;
    }

    document.getElementById("total").innerText = `Total: Rp ${totalPrice}`;
}

// Fungsi untuk reset keranjang
function resetCart() {
    cart = {};
    document.getElementById("message").innerText = '';
    updateCart();
}

// Fungsi untuk memproses pembayaran
function processPayment() {
    const amountPaid = parseInt(document.getElementById("amountPaid").value);
    
    if (isNaN(amountPaid) || amountPaid < totalPrice) {
        document.getElementById("message").innerText = "Pembayaran tidak cukup atau tidak valid!";
    } else {
        const change = amountPaid - totalPrice;
        document.getElementById("message").innerText = `Pembayaran Berhasil! Kembalian Anda: Rp ${change}`;
    }
}

// Event listener untuk input judul buku
document.getElementById("bukuInput").addEventListener("keypress", function(event) {
    if (event.key === 'Enter') {
        addToCart(event.target.value);
        event.target.value = '';  
    }
});

// Jalankan fungsi untuk menampilkan produk saat halaman dimuat
displayProducts();
