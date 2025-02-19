let api;
let ticks;
let isAnalyzing = false;
let prediction = null;
let mainValue = 939.79;
let timer = 20;
let overUnderRatio = { over: 40, under: 60 };

const volatilitySelect = document.getElementById('volatilitySelect');
const mainValueElement = document.getElementById('mainValue');
const predictBtn = document.getElementById('predictBtn');
const predictionElement = document.getElementById('prediction');
const resultText = document.getElementById('resultText');
const overRatioElement = document.getElementById('overRatio');
const underRatioElement = document.getElementById('underRatio');
const overButtons = document.getElementById('overButtons');
const underButtons = document.getElementById('underButtons');
const startAnalysisBtn = document.getElementById('startAnalysisBtn');
const toggleAnalysisBtn = document.getElementById('toggleAnalysisBtn');
const wsStatusElement = document.getElementById('wsStatus');
const wsErrorElement = document.getElementById('wsError');
const signoutBtn = document.getElementById('signoutBtn');

// Function to update main value and numbers
const updateMainValue = (value) => {
  mainValue = value;
  mainValueElement.textContent = value.toFixed(2);
  updatePredictionNumbers();
};

// Function to start and stop analysis
const toggleAnalysis = () => {
  if (isAnalyzing) {
    stopAnalysis();
  } else {
    startAnalysis();
  }
};

// Start analysis
const startAnalysis = () => {
  isAnalyzing = true;
  startAnalysisBtn.classList.add('bg-gray-600');
  startAnalysisBtn.classList.remove('bg-green-600');
  startAnalysisBtn.textContent = 'Stop Analysis';
  wsStatusElement.textContent = 'Connecting...';
  connectToDerivAPI();
};

// Stop analysis
const stopAnalysis = () => {
  isAnalyzing = false;
  startAnalysisBtn.classList.remove('bg-gray-600');
  startAnalysisBtn.classList.add('bg-green-600');
  startAnalysisBtn.textContent = 'Start Analysis';
  wsStatusElement.textContent = 'Disconnected';
  if (ticks) {
    ticks.unsubscribe();
  }
  if (api) {
    api.disconnect();
  }
};

// Connect to Deriv API
const connectToDerivAPI = () => {
  api = new window.DerivAPIBasic({
    endpoint: "ws.derivws.com",
    app_id: 1089,
    lang: "EN",
  });

  api.onOpen().subscribe(() => {
    wsStatusElement.textContent = 'Connected';
    ticks = api.subscribe({ ticks: volatilitySelect.value });
    ticks.subscribe((tick) => {
      updateMainValue(Number.parseFloat(tick.quote));
    });
  });

  api.onClose().subscribe(() => {
    wsStatusElement.textContent = 'Disconnected';
    if (isAnalyzing) {
      setTimeout(() => {
        connectToDerivAPI();
      }, 2000);
    }
  });

  api.onError().subscribe((error) => {
    console.error('API error:', error);
    wsStatusElement.textContent = 'Disconnected';
    wsErrorElement.classList.remove('hidden');
    wsErrorElement.textContent = `Error: ${error}`;
  });

  api.connect();
};

// Update prediction numbers
const updatePredictionNumbers = () => {
  const lastDigit = Math.floor(mainValue) % 10;
  prediction = lastDigit;
  predictionElement.textContent = prediction;
  timer = 20;
  predictBtn.disabled = true;

  setTimeout(() => {
    resultText.textContent = lastDigit === prediction ? 'Won' : 'Lost';
  }, timer * 1000);
};

// Select volatility
const handleVolatilityChange = () => {
  if (isAnalyzing) {
    updatePredictionNumbers();
  }
};

// Select "Over" or "Under"
const handleOverUnderSelect = (type, num) => {
  const newOver = Math.floor(Math.random() * 70) + 30;
  overUnderRatio = { over: newOver, under: 100 - newOver };
  overRatioElement.textContent = `${overUnderRatio.over}%`;
  underRatioElement.textContent = `${overUnderRatio.under}%`;
  alert(`Selected ${type} ${num}`);
};

// Sign out
const handleSignout = () => {
  alert('Signing out...');
  window.location.href = '/login';
};

// Initial Setup
volatilitySelect.addEventListener('change', handleVolatilityChange);
startAnalysisBtn.addEventListener('click', toggleAnalysis);
signoutBtn.addEventListener('click', handleSignout);

toggleAnalysisBtn.addEventListener('click', toggleAnalysis);

// Generate over/under buttons
const generateOverUnderButtons = () => {
  for (let i = 1; i <= 8; i++) {
    const overBtn = document.createElement('button');
    overBtn.classList.add('bg-blue-400', 'hover:bg-blue-500', 'text-white', 'py-2', 'px-4', 'rounded');
    overBtn.textContent = i;
    overBtn.onclick = () => handleOverUnderSelect('OVER', i);
    overButtons.appendChild(overBtn);

    const underBtn = document.createElement('button');
    underBtn.classList.add('bg-blue-400', 'hover:bg-blue-500', 'text-white', 'py-2', 'px-4', 'rounded');
    underBtn.textContent = i;
    underBtn.onclick = () => handleOverUnderSelect('UNDER', i);
    underButtons.appendChild(underBtn);
  }
};

// Initialize
generateOverUnderButtons();
