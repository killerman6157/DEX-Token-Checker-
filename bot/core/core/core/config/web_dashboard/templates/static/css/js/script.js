// web_dashboard/static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    fetchHistory();
});

async function checkToken() {
    const contractAddress = document.getElementById('contractAddress').value.trim();
    const resultDiv = document.getElementById('result');

    if (!contractAddress) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'result-box error';
        resultDiv.innerText = 'Don Allah ka saka contract address.';
        return;
    }

    resultDiv.style.display = 'block';
    resultDiv.className = 'result-box';
    resultDiv.innerText = 'Muna binciken token... Da fatan za a jira.';

    try {
        const response = await fetch('/api/check_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ contract_address: contractAddress })
        });

        const data = await response.json();

        if (response.ok) {
            const rugPullClass = data.rug_pull_risk === 'LOW' ? 'low-risk' : 'high-risk';
            resultDiv.innerHTML = `
                <strong>Sakamakon Binciken Token:</strong><br>
                <strong>Sunan Token:</strong> <code>${data.token_name || 'N/A'}</code><br>
                <strong>Contract Address:</strong> <code>${data.contract_address}</code><br>
                <strong>Rug Pull Risk:</strong> <span class="${rugPullClass}">${data.rug_pull_risk}</span><br>
                <strong>Ownership Renounced:</strong> ${data.ownership_renounced ? '✅ E Haka Ne' : '❌ A\'a'}<br>
                <strong>LP Locked:</strong> ${data.lp_locked ? '✅ E Haka Ne' : '❌ A\'a'}<br>
                <strong>Adadin Masu Riƙe (Holders):</strong> <code>${data.holders_count || 'N/A'}</code><br>
                <strong>Verified Supply:</strong> <code>${data.total_supply || 'N/A'}</code><br>
            `;
            resultDiv.className = 'result-box';
            fetchHistory(); // Refresh history after new check
        } else {
            resultDiv.className = 'result-box error';
            resultDiv.innerText = `Kuskure: ${data.error || 'Wani abu ya faru.'}`;
        }
    } catch (error) {
        resultDiv.className = 'result-box error';
        resultDiv.innerText = `An samu kuskure yayin kiran API: ${error.message}`;
    }
}

async function fetchHistory() {
    const historyTableBody = document.querySelector('#historyTable tbody');
    historyTableBody.innerHTML = ''; // Clear existing rows

    try {
        const response = await fetch('/api/history');
        const history = await response.json();

        history.forEach(item => {
            const row = historyTableBody.insertRow();
            const rugPullClass = item.rug_pull_risk === 'LOW' ? 'low-risk' : 'high-risk';
            row.innerHTML = `
                <td>${new Date(item.timestamp).toLocaleString()}</td>
                <td>${item.token_name || 'N/A'}</td>
                <td><code>${item.contract_address}</code></td>
                <td class="${rugPullClass}">${item.rug_pull_risk || 'N/A'}</td>
                <td>${item.ownership_renounced ? '✅' : '❌'}</td>
                <td>${item.lp_locked ? '✅' : '❌'}</td>
                <td>${item.holders_count || 'N/A'}</td>
                <td>${item.total_supply || 'N/A'}</td>
            `;
        });
    } catch (error) {
        console.error("Kuskure yayin fetching history:", error);
        // Optionally display an error message in the history section
    }
  }
      
