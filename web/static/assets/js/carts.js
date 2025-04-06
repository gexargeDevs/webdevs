document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartItemsList = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');
    const cartCountElement = document.getElementById('cart-count');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // გამოსახვა გვერდის ჩატვირთვისას
    updateCartDisplay();

    // დამატება კალათაში
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.dataset.id;
            const name = this.dataset.name;
            const price = parseFloat(this.dataset.price);
            const image = this.dataset.image;
            
            addToCart(id, name, price, image);
            updateCartDisplay();
        });
    });

    function addToCart(id, name, price, image) {
        const existingItem = cart.find(item => item.id === id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: id,
                name: name,
                price: price,
                image: image,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function removeFromCart(id) {
        cart = cart.filter(item => item.id !== id);
        saveCart();
        updateCartDisplay();
    }

    function updateQuantity(id, quantity) {
        const item = cart.find(item => item.id === id);
        
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                removeFromCart(id);
            } else {
                saveCart();
                updateCartDisplay();
            }
        }
    }

    function saveCart() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function updateCartDisplay() {
        // კალათის განახლება UI-ზე
        if (cartItemsList && cartTotalElement) {
            cartItemsList.innerHTML = '';
            let total = 0;
            
            cart.forEach(item => {
                const listItem = document.createElement('li');
                listItem.classList.add('cart-item');
                listItem.innerHTML = `
                    <img src="/${item.image}" alt="${item.name}" style="width: 50px; height: 50px; margin-right: 10px;">
                    <span>${item.name} (${item.price} ლარი) × 
                    <input type="number" value="${item.quantity}" min="1" data-id="${item.id}" class="quantity-input"></span>
                    <button class="remove-from-cart" data-id="${item.id}">წაშლა</button>
                `;
                cartItemsList.appendChild(listItem);
                total += item.price * item.quantity;
            });
            
            cartTotalElement.textContent = total.toFixed(2);
        }
        
        // კალათის რაოდენობის განახლება
        if (cartCountElement) {
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            cartCountElement.textContent = totalItems;
        }
        
        // დამატებული ღილაკების მოსმენა
        document.querySelectorAll('.remove-from-cart').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.dataset.id;
                removeFromCart(id);
            });
        });
        
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const id = this.dataset.id;
                const quantity = this.value;
                updateQuantity(id, quantity);
            });
        });
    }
});