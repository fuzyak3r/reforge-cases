// Global variables
let user = null;
let selectedAmount = null;

// Check authentication status
function checkAuth() {
    fetch('/api/user')
        .then(response => {
            if (response.status === 401) {
                // Not logged in
                $('#profile-card').hide();
                $('#login-card').show();
                return { authenticated: false };
            }
            return response.json();
        })
        .then(data => {
            if (data.error || !data.steam_id) {
                // Not logged in
                $('#profile-card').hide();
                $('#login-card').show();
            } else {
                // Logged in
                user = data;
                displayUserProfile();
                $('#login-card').hide();
                $('#profile-card').show();
                $('#login-item').html(`<span class="nav-link">Balance: $${data.balance.toFixed(2)}</span>`);
            }
        })
        .catch(error => {
            console.error('Auth check error:', error);
            $('#profile-card').hide();
            $('#login-card').show();
        });
}

// Display user profile
function displayUserProfile() {
    if (!user) return;
    
    $('#profile-avatar').attr('src', user.avatar);
    $('#profile-username').text(user.username);
    $('#profile-balance').text(user.balance.toFixed(2));
    $('#profile-inventory-count').text(user.inventory_count);
    $('#profile-joined').text(formatDate(user.created_at));
}

// Format date string
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

// Add funds to account
function addFunds() {
    if (!selectedAmount) return;
    
    fetch('/api/add-funds', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            amount: selectedAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Update user balance
        user.balance += selectedAmount;
        $('#profile-balance').text(user.balance.toFixed(2));
        $('#login-item').html(`<span class="nav-link">Balance: $${user.balance.toFixed(2)}</span>`);
        
        // Reset and close modal
        selectedAmount = null;
        $('#selected-amount').text('0');
        $('#confirm-funds-btn').prop('disabled', true);
        $('.fund-option').removeClass('active');
        $('#fundsModal').modal('hide');
    })
    .catch(error => {
        console.error('Error adding funds:', error);
        alert('Error adding funds. Please try again.');
    });
}

// Initialize page
$(document).ready(function() {
    checkAuth();
    
    // Add funds button
    $('#add-funds-btn').click(function() {
        selectedAmount = null;
        $('#selected-amount').text('0');
        $('#confirm-funds-btn').prop('disabled', true);
        $('.fund-option').removeClass('active');
        $('#fundsModal').modal('show');
    });
    
    // Fund option selection
    $('.fund-option').click(function() {
        $('.fund-option').removeClass('active');
        $(this).addClass('active');
        
        selectedAmount = parseFloat($(this).data('amount'));
        $('#selected-amount').text(selectedAmount);
        $('#confirm-funds-btn').prop('disabled', false);
    });
    
    // Confirm funds button
    $('#confirm-funds-btn').click(addFunds);
});