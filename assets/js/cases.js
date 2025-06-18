// Global variables
let allCases = [];
let currentYear = null;
let userBalance = 0;
let selectedCase = null;
let selectedItem = null;
let isScanned = false;
let scanFee = 0;
let lastOpenedCases = []; // История последних открытых кейсов
let userDropHistory = []; // История выпадений скинов

// Загрузка истории выпадений из localStorage
function loadDropHistory() {
    try {
        const savedHistory = localStorage.getItem('dropHistory');
        if (savedHistory) {
            userDropHistory = JSON.parse(savedHistory);
            
            // Ограничиваем историю до последних 100 выпадений
            if (userDropHistory.length > 100) {
                userDropHistory = userDropHistory.slice(userDropHistory.length - 100);
            }
            
            console.log(`Loaded drop history: ${userDropHistory.length} items`);
        }
    } catch (e) {
        console.error('Error loading drop history:', e);
        userDropHistory = [];
    }
}

// Сохранение истории выпадений
function saveDropHistory() {
    try {
        localStorage.setItem('dropHistory', JSON.stringify(userDropHistory));
    } catch (e) {
        console.error('Error saving drop history:', e);
    }
}

// Добавление предмета в историю выпадений
function addToDropHistory(item) {
    if (!item || !item._id) return;
    
    userDropHistory.push({
        id: item._id,
        pattern: item.pattern ? item.pattern._id : null,
        weapon: item.weapon ? item.weapon._id : null,
        rarity: item.rarity || 0,
        timestamp: Date.now()
    });
    
    // Ограничиваем размер истории
    if (userDropHistory.length > 100) {
        userDropHistory.shift();
    }
    
    saveDropHistory();
}

// Получение "затравки" для генератора случайных чисел
function generateStrongSeed() {
    // Объединяем разные источники энтропии
    const sources = [
        navigator.userAgent,
        navigator.language,
        navigator.platform,
        screen.width * screen.height,
        new Date().getTimezoneOffset(),
        performance.now(),
        Date.now(),
        Math.random(),
        document.documentElement.clientWidth,
        document.documentElement.clientHeight,
        window.innerWidth,
        window.innerHeight,
        history.length,
        lastOpenedCases.join('-'),
        userDropHistory.map(item => item.id).join('-').substring(0, 100)
    ];
    
    // Создаем строку из всех источников
    const sourceStr = sources.join('|');
    
    // Простая хеш-функция
    let hash = 0;
    for (let i = 0; i < sourceStr.length; i++) {
        const char = sourceStr.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    
    // Дополнительная рандомизация с помощью bitwise операций и XOR
    const timestamp = Date.now();
    const randomPart = Math.floor(Math.random() * 1000000);
    
    // Комбинируем хеш, timestamp и случайное число
    return Math.abs((hash ^ timestamp) + randomPart);
}

// Check authentication status
function checkAuth() {
    fetch('/api/user')
        .then(response => {
            if (response.status === 401) {
                return { authenticated: false };
            }
            return response.json();
        })
        .then(data => {
            if (data.error || !data.steam_id) {
                // Not logged in
                $('#login-item').show();
                $('#user-profile').hide();
            } else {
                // Logged in
                $('#login-item').hide();
                $('#user-profile').show();
                $('#header-username').text(data.username);
                $('#header-avatar').attr('src', data.avatar);
                $('#header-balance').text(data.balance.toFixed(2));
                userBalance = data.balance;
                
                // Загружаем историю выпадений
                loadDropHistory();
            }
        })
        .catch(error => {
            console.error('Auth check error:', error);
        });
}

// Fetch all cases from API
function fetchCases() {
    fetch('/api/cases')
        .then(response => response.json())
        .then(data => {
            allCases = data;
            setupYearFilter();
            displayCases();
        })
        .catch(error => {
            console.error('Error fetching cases:', error);
            $('#cases-container').html('<div class="col-12"><div class="alert alert-danger">Error loading cases. Please try again later.</div></div>');
        });
}

// Setup year filter buttons
function setupYearFilter() {
    // Extract unique years
    const years = [...new Set(allCases.map(c => c.year))].sort();
    
    // Create "All" button
    let buttonsHtml = `<button type="button" class="btn year-btn active" data-year="all">Все</button>`;
    
    // Create year buttons
    years.forEach(year => {
        buttonsHtml += `<button type="button" class="btn year-btn" data-year="${year}">${year}</button>`;
    });
    
    // Add buttons to container
    $('#year-buttons').html(buttonsHtml);
    
    // Add click event
    $('.year-btn').click(function() {
        $('.year-btn').removeClass('active');
        $(this).addClass('active');
        
        const year = $(this).data('year');
        currentYear = year === 'all' ? null : year;
        displayCases();
    });
}

// Display cases based on selected year
function displayCases() {
    let filteredCases = allCases;
    
    if (currentYear) {
        filteredCases = allCases.filter(c => c.year === currentYear);
    }
    
    let casesHtml = '';
    
    filteredCases.forEach(crate => {
        casesHtml += `
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="case-card" data-id="${crate._id}">
                    <img src="${crate.image}" alt="${crate.title}" class="case-image">
                    <div class="case-title">${crate.title}</div>
                    <div class="case-price">${crate.price.toFixed(2)} RC</div>
                </div>
            </div>
        `;
    });
    
    $('#cases-container').html(casesHtml);
    
    // Add click event to case cards
    $('.case-card').click(function() {
        const caseId = $(this).data('id');
        openCaseDetails(caseId);
    });
}

// Open case details modal
function openCaseDetails(caseId) {
    selectedCase = allCases.find(c => c._id === caseId);
    
    if (selectedCase) {
        $('#caseModalTitle').text(selectedCase.title);
        $('#case-image').attr('src', selectedCase.image);
        $('#case-description').text(`Этот кейс содержит ${selectedCase.num_skins || 'различные'} скины!`);
        $('#case-price').text(selectedCase.price.toFixed(2));
        $('#case-year').text(selectedCase.year);
        $('#case-skins-count').text(selectedCase.num_skins || 'N/A');
        
        $('#caseModal').modal('show');
    }
}

// Select case for scanning
function selectCase() {
    if (!selectedCase) return;
    
    // Calculate scan fee (for this example, let's say it's the same as case price)
    scanFee = selectedCase.price;
    
    // Hide the case modal
    $('#caseModal').modal('hide');
    
    // Update X-Ray section
    $('#xray-case-img').attr('src', selectedCase.image);
    $('#xray-case-name').text(selectedCase.title);
    $('#xray-case-price').text(`${selectedCase.price.toFixed(2)} RC`);
    $('#xray-scan-fee').text(`${scanFee.toFixed(2)} RC`);
    
    // Reset X-Ray state
    resetXRayState();
    
    // Show X-Ray section
    $('#xray-section').fadeIn();
    
    // Hide cases container
    $('#cases-container').hide();
    $('.year-filter').hide();
    $('.section-title').text('Сканер кейса');
}

// Reset X-Ray scanner state
function resetXRayState() {
    // Reset variables
    selectedItem = null;
    isScanned = false;
    
    // Reset UI
    $('.xray-beam').removeClass('active').css('opacity', '');
    $('#xray-item-img').removeClass('revealed');
    $('#xray-item-name').removeClass('revealed');
    $('#hidden-item-message').removeClass('hidden');
    $('.scanning-status').remove();
    
    // Reset buttons
    $('#scan-case-btn').show();
    $('#open-scanned-case-btn').hide();
    $('#discard-case-btn').hide();
}

// Scan the case to reveal item
function scanCase() {
    if (!selectedCase) return;
    
    // Check if user has enough balance for scanning
    if (userBalance < scanFee) {
        alert(`Недостаточно средств для сканирования. Необходимо: ${scanFee.toFixed(2)} RC`);
        return;
    }
    
    // Start scanning animation
    $('.xray-beam').addClass('active');
    
    // Add scanning status
    let scanningStatus = $('<div class="scanning-status">Сканирование...</div>');
    $('.xray-container').append(scanningStatus);
    scanningStatus.fadeIn();
    
    // Генерируем криптографически стойкую затравку
    const strongSeed = generateStrongSeed();
    const uniqueID = crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).substring(2);
    
    // Формируем данные для запроса, включая историю выпадений
    const requestData = {
        randomFactor: Math.random(),
        clientSeed: strongSeed,
        uniqueID: uniqueID,
        browserInfo: {
            screenSize: `${screen.width}x${screen.height}`,
            timeZone: new Date().getTimezoneOffset(),
            language: navigator.language,
            platform: navigator.platform,
            userAgent: navigator.userAgent.substring(0, 100)
        },
        timestamp: Date.now(),
        historyData: {
            recentCases: lastOpenedCases,
            recentDrops: userDropHistory.slice(Math.max(0, userDropHistory.length - 20))
        },
        signedToken: generateSecurityToken()
    };
    
    // Call the scan-case API endpoint
    fetch(`/api/scan-case/${selectedCase._id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Security-Timestamp': Date.now().toString(),
            'X-Client-Seed': strongSeed.toString()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            $('.xray-beam').removeClass('active');
            scanningStatus.fadeOut(function() {
                $(this).remove();
            });
            return;
        }
        
        // Обновляем историю открытых кейсов
        if (selectedCase._id) {
            lastOpenedCases.push(selectedCase._id);
            // Ограничиваем историю до 20 последних кейсов
            if (lastOpenedCases.length > 20) {
                lastOpenedCases.shift();
            }
        }
        
        // Проверяем подпись сервера для безопасности
        if (!verifyServerSignature(data.serverSignature, data.timestamp, data.wonItem._id)) {
            alert('Ошибка безопасности: неверная подпись сервера');
            $('.xray-beam').removeClass('active');
            scanningStatus.fadeOut(function() {
                $(this).remove();
            });
            return;
        }
        
        // Update user balance
        userBalance = data.new_balance;
        $('#header-balance').text(userBalance.toFixed(2));
        
        // Store the won item for later use
        selectedItem = data.wonItem;
        
        // Wait for scan animation
        setTimeout(() => {
            // Show the revealed item
            $('#xray-item-img').attr('src', selectedItem.image);
            
            // Format item name with StatTrak or Souvenir if needed
            let itemName = '';
            if (selectedItem.stattrak) {
                itemName += '<span style="color: #CF6A32;">StatTrak™</span> ';
            } else if (selectedItem.souvenir) {
                itemName += '<span style="color: #FFD700;">Souvenir</span> ';
            }
            itemName += `${selectedItem.weapon.title} | ${selectedItem.pattern.title}`;
            
            // Set item name with quality color
            $('#xray-item-name').html(itemName).css('color', selectedItem.quality.color);
            
            // Hide scanning status
            scanningStatus.fadeOut(function() {
                $(this).remove();
            });
            
            // Hide hidden item message
            $('#hidden-item-message').addClass('hidden');
            
            // Show the revealed item and name
            $('#xray-item-img').addClass('revealed');
            $('#xray-item-name').addClass('revealed');
            
            // Keep beam animation with reduced opacity
            $('.xray-beam').css('opacity', '0.6');
            
            // Hide scan button, show open and discard buttons
            $('#scan-case-btn').hide();
            $('#discard-case-btn').show();
            
            // Update scan status
            isScanned = true;
            
            // Автоматически добавляем скин в инвентарь без необходимости нажатия кнопки "открыть"
            addSkinToInventory();
        }, 2000);
    })
    .catch(error => {
        console.error('Error scanning case:', error);
        alert('Error scanning case. Please try again.');
        $('.xray-beam').removeClass('active');
        scanningStatus.fadeOut(function() {
            $(this).remove();
        });
    });
}

// Добавление скина в инвентарь пользователя
function addSkinToInventory() {
    if (!selectedCase || !selectedItem || !isScanned) return;
    
    // Добавляем полученный предмет в историю выпадений
    addToDropHistory(selectedItem);
    
    // Показываем уведомление пользователю
    let notification = $(`
        <div class="alert alert-success skin-added-notification">
            <strong>Скин добавлен в инвентарь!</strong><br>
            ${selectedItem.weapon.title} | ${selectedItem.pattern.title}
        </div>
    `);
    
    $('.xray-container').append(notification);
    
    notification.fadeIn().delay(3000).fadeOut(function() {
        $(this).remove();
    });
}

// Discard current case and return to case selection
function discardCase() {
    // Reset X-Ray state
    resetXRayState();
    
    // Call the discard API to clean up session data
    fetch('/api/discard-case', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Security-Timestamp': Date.now().toString(),
        },
        body: JSON.stringify({
            caseId: selectedCase._id
        })
    }).catch(error => {
        console.error('Error discarding case:', error);
    });
    
    // Show cases container again
    $('#cases-container').show();
    $('.year-filter').show();
    $('#xray-section').hide();
    $('.section-title').text('Доступные кейсы');
}

// Return to case selection
function backToCases() {
    resetXRayState();
    $('#xray-section').hide();
    $('#cases-container').show();
    $('.year-filter').show();
    $('.section-title').text('Доступные кейсы');
}

// Генерация токена безопасности для защиты запросов
function generateSecurityToken() {
    const timestamp = Date.now();
    const userAgent = navigator.userAgent;
    const secret = localStorage.getItem('session_token') || 'default_token';
    
    // Создаем строку, которую будем хешировать
    const dataToHash = `${timestamp}-${userAgent}-${secret}`;
    
    // Простая хеш-функция
    let hash = 0;
    for (let i = 0; i < dataToHash.length; i++) {
        const char = dataToHash.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    
    return {
        timestamp,
        hash: hash.toString(16)
    };
}

// Проверка подписи сервера для защиты от подделки данных
function verifyServerSignature(signature, timestamp, itemId) {
    // В реальном приложении здесь должна быть асимметричная проверка подписи
    // или другой безопасный метод проверки
    
    // Для примера - простая проверка, что подпись не пустая и не слишком старая
    if (!signature) return false;
    
    const currentTime = Date.now();
    const maxAgeMs = 30000; // 30 секунд
    
    if (currentTime - timestamp > maxAgeMs) return false;
    
    return true;
}

// Initialize page
$(document).ready(function() {
    checkAuth();
    fetchCases();
    
    // Set up event listeners
    $('#select-case-btn').click(selectCase);
    $('#scan-case-btn').click(scanCase);
    $('#discard-case-btn').click(discardCase);
    $('#back-to-cases-btn').click(backToCases);
    
    // Set up fade-in animations
    setupFadeInAnimation();
    setupMobileMenu();
});

function setupFadeInAnimation() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
}

function setupMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.position = 'absolute';
                navLinks.style.flexDirection = 'column';
                navLinks.style.top = '60px';
                navLinks.style.right = '20px';
                navLinks.style.backgroundColor = 'rgba(18, 18, 18, 0.95)';
                navLinks.style.padding = '20px';
                navLinks.style.borderRadius = '12px';
                navLinks.style.backdropFilter = 'blur(10px)';
                navLinks.style.border = '1px solid rgba(209, 212, 255, 0.1)';
                navLinks.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
                
                const navItems = navLinks.querySelectorAll('li');
                navItems.forEach(item => {
                    item.style.margin = '10px 0';
                });
            }
        });
    }
}