
    function generateQuery() {
    const sqlType = document.getElementById('sql-type').value;
    const prompt = document.getElementById('prompt-input').value;
    let query = '';

    if (prompt.toLowerCase().includes('highest paid employee')) {
        query = `SELECT * FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);`;
    } else {
        query = `-- SQL query for ${sqlType} based on prompt: ${prompt}`;
    }

    document.getElementById('generated-output').innerText = query;

    // Create a new textbox
    const newTextbox = document.createElement('textarea');
    newTextbox.rows = 4;
    newTextbox.style.width = '100%';
    newTextbox.style.border = 'none';
    newTextbox.style.outline = 'none';
    newTextbox.style.resize = 'none';
    newTextbox.style.fontSize = '24px';
    newTextbox.style.fontFamily = "'Inria Sans', sans-serif";
    newTextbox.style.color = '#808080';
    newTextbox.value = query;

    // Append the new textbox to the container
    const container = document.querySelector('.main-content');
    container.appendChild(newTextbox);
}

document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const placeholderText = 'Enter prompt to generate query eg: give me highest paid employee';

    promptInput.value = placeholderText;
    promptInput.style.color = '#808080';

    promptInput.addEventListener('focus', () => {
        if (promptInput.value === placeholderText) {
            promptInput.value = '';
            promptInput.style.color = '#000000';
        }
    });

    promptInput.addEventListener('blur', () => {
        if (promptInput.value === '') {
            promptInput.value = placeholderText;
            promptInput.style.color = '#808080';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const csvFileInput = document.getElementById('csv-file');
    const csvLabel = document.getElementById('csv-label');
    const excelFileInput = document.getElementById('excel-file');
    const excelLabel = document.getElementById('excel-label');
    const inputPrompt = document.getElementById('input-prompt');

    // inputPrompt.disabled = true;

    // Event listener for CSV file input
    csvFileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileName = this.files[0].name;
            csvLabel.textContent = fileName;  // Update label with the file name
            excelFileInput.disabled = true;   // Disable the Excel input
            excelLabel.classList.add('disabled'); // Add disabled class to grey out label
        } else {
            csvLabel.textContent = "Upload CSV File"; // Reset label if no file is selected
            excelFileInput.disabled = false;  // Re-enable the Excel input
            excelLabel.classList.remove('disabled'); // Remove disabled class
        }
    });

    // Event listener for Excel file input
    excelFileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileName = this.files[0].name;
            excelLabel.textContent = fileName;  // Update label with the file name
            csvFileInput.value = "";            // Unselect CSV file
            csvLabel.textContent = "Upload CSV File"; // Reset CSV label
            csvFileInput.disabled = true;   // Disable CSV input
            csvLabel.classList.add('disabled'); // Add disabled class to grey out label
        } else {
            excelLabel.textContent = "Upload Excel File"; // Reset label if no file is selected
        }

        // Disable CSV input if Excel file is selected
        csvFileInput.disabled = this.files.length > 0;   
        if (csvFileInput.disabled) {
            csvLabel.classList.add('disabled'); // Add disabled class to grey out label
        } else {
            csvLabel.classList.remove('disabled'); // Remove disabled class
        }
    });
    
    inputPrompt.addEventListener('focus', function() {
        if (this.disabled) {
            alert("Please select a SQL Server and upload a file before entering text."); // Show alert if textarea is disabled
            this.blur(); // Remove focus to prevent typing
        }
    });
});

function copyToClipboard(textareaId) {
    const textarea = document.getElementById(textareaId);
    textarea.select();
    document.execCommand("copy");
    alert("Copied to clipboard!"); // Optional: alert message
}

window.onpopstate = function () {
    window.history.go(1);
};









function enableCSVUpload() {
    document.getElementById('csv-file').disabled = false;
    document.getElementById('csv-submit').disabled = false;
    document.getElementById('excel-file').disabled = true;
    document.getElementById('excel-submit').disabled = true;
}

function enableExcelUpload() {
    document.getElementById('csv-file').disabled = true;
    document.getElementById('csv-submit').disabled = true;
    document.getElementById('excel-file').disabled = false;
    document.getElementById('excel-submit').disabled = false;
}

function validateCSVFile(input) {
    const file = input.files[0];
    const maxSize = 5 * 1024 * 1024; 
    console.log("hello");
    console.log(file);
    if (file && !file.name.endsWith('.csv')) {
        alert('Invalid file format. Only CSV files are allowed.');
        input.value = ''; // Clear the input
    }
    if (file.size > maxSize) {
        alert('File size exceeds 5 MB. Please upload a smaller file.');
        input.value = ''; // Clear the input if the file is too large
        return;
    }
    console.log("File is valid:", file.name);
}

function validateExcelFile(input) {
    const file = input.files[0];
    const maxSize = 5 * 1024 * 1024; 
    if (file && !file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
        alert('Invalid file format. Only Excel files are allowed.');
        input.value = ''; // Clear the input
    }
    if (file.size > maxSize) {
        alert('File size exceeds 5 MB. Please upload a smaller file.');
        input.value = ''; // Clear the input if the file is too large
        return;
    }
    console.log("File is valid:", file.name, file.size);
}

function validateForm() {
    const fileInput = document.getElementById('csv-file');
    console.log("hello")
    // Check if a file is selected
    if (!fileInput.files.length) {
        alert('Please select a file before submitting.');
        event.preventDefault(); 
    }
}






