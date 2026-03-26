const pricing = {
    "gpt-4o": { input: 0.003, output: 0.015 },
    "claude": { input: 0.002, output: 0.012 },
    "gemini": { input: 0.0025, output: 0.013 }
  };
  
  function calculateCost() {
    const model = document.getElementById("model").value;
    const tokensPerRequest = parseInt(document.getElementById("tokens").value) || 0;
    const requestsPerDay = parseInt(document.getElementById("requests").value) || 0;
    const daysPerMonth = parseInt(document.getElementById("days").value) || 0;
  
    const monthlyRequests = requestsPerDay * daysPerMonth;
    const totalTokens = tokensPerRequest * monthlyRequests;
  
    const costInput = (totalTokens / 1000) * pricing[model].input;
    const costOutput = (totalTokens / 1000) * pricing[model].output;
    const totalCost = costInput + costOutput;
  
    document.getElementById("result").innerHTML = 
      `Estimated Monthly Cost: $${totalCost.toFixed(2)}`;
  }