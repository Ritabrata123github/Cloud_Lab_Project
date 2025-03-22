// Replace with your actual API Gateway URLs
const GET_PATIENTS_URL = 'https://mg6mted8w9.execute-api.ap-south-1.amazonaws.com/prod/get_patients';
const POST_PATIENT_URL = 'https://mg6mted8w9.execute-api.ap-south-1.amazonaws.com/prod/store_patient';

// Function to fetch all patients
document.getElementById('fetch-patients').addEventListener('click', async () => {
    const outputDiv = document.getElementById('output');
    try {
        const response = await fetch(GET_PATIENTS_URL);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        // Create a table to display patient records
        let tableHTML = '<table>';
        tableHTML += '<tr><th>Patient ID</th><th>Name</th><th>Age</th><th>Medical History</th></tr>';
        data.forEach(patient => {
            tableHTML += `<tr>
                <td>${patient.patient_id}</td>
                <td>${patient.name}</td>
                <td>${patient.age}</td>
                <td>${patient.medical_history}</td>
            </tr>`;
        });
        tableHTML += '</table>';

        outputDiv.innerHTML = tableHTML; // Display the table
    } catch (error) {
        console.error('Error fetching patients:', error);
        outputDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

// Function to save a patient
document.getElementById('save-patient').addEventListener('click', async () => {
    const patientForm = document.forms['patient-form'];
    const patientData = {
        patient_id: patientForm['patient_id'].value,
        name: patientForm['name'].value,
        age: parseInt(patientForm['age'].value),
        medical_history: patientForm['medical_history'].value
    };

    const outputDiv = document.getElementById('output');
    try {
        const response = await fetch(POST_PATIENT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        outputDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
    } catch (error) {
        console.error('Error saving patient:', error);
        outputDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});
