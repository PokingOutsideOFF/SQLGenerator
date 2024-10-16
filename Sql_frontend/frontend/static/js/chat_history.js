function changeSessionStatus(){
    sessionStorage.setItem('loggedOut', 'True')
    sessionStorage.setItem('isLoggedIn', 'False')
    {{request.session.username = 'User'}}
}


const chatData = JSON.parse(document.getElementById('chat-data').textContent);

function filterChatHistory() {
    const filter = document.getElementById('filter').value;
    const tbody = document.querySelector('.chat-history-table tbody');  
    // Clear existing rows
    tbody.innerHTML = '';

    // Filter the chat data based on the selected SQL type
    const filteredData = chatData.filter(entry => {
        return filter === 'all' || entry.sql_server === filter;
    });

    // Populate the table with filtered data
    if (filteredData.length > 0) {
        filteredData.forEach(entry => {
            const row = `<tr>
                <td>${entry.prompt}</td>
                <td>${entry.generated_query}</td>
                <td>${entry.sql_server}</td>
                <td>${entry.timestamp}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="4">No chat history found.</td></tr>';
    }
}
