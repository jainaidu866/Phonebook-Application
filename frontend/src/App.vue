<template>
  <div class="app-container">
    <div class="card">
      <header class="header">
        <h1>Phonebook App</h1>
        <p>Manage your professional contacts efficiently.</p>
      </header>
      
      <section class="form-section">
        <div class="input-group">
          <input v-model="form.name" placeholder="Contact Name" required />
          <input v-model="form.phone_number" placeholder="Phone Number" required />
          <button @click="submitContact" class="btn-primary">Add Contact</button>
        </div>
      </section>

      <section class="list-section">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contact in contacts" :key="contact.id">
              <td class="font-bold">{{ contact.name }}</td>
              <td>{{ contact.phone_number }}</td>
              <td class="text-center">
                <button @click="deleteContact(contact.id)" class="btn-danger">Delete</button>
              </td>
            </tr>
            <tr v-if="contacts.length === 0">
              <td colspan="3" class="text-center muted">No contacts found. Add one above!</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const contacts = ref([])
const form = ref({ name: '', phone_number: '' })

// Get all contacts from the backend
const getContacts = async () => {
  const response = await axios.get('http://localhost:8000/contacts')
  contacts.value = response.data
}

// Send a new contact to the backend
const submitContact = async () => {
  if (!form.value.name || !form.value.phone_number) return alert("Please fill in both fields.")
  await axios.post('http://localhost:8000/contacts', form.value)
  form.value = { name: '', phone_number: '' }
  getContacts()
}

// Delete a contact
const deleteContact = async (id) => {
  if(confirm("Are you sure you want to delete this contact?")) {
    await axios.delete(`http://localhost:8000/contacts/${id}`)
    getContacts()
  }
}

onMounted(getContacts)
</script>

<style scoped>
/* Professional Modern CSS */
:global(body) {
  background-color: #f0f2f5;
  margin: 0;
  color: #1c1e21;
}

.app-container {
  display: flex;
  justify-content: center;
  padding: 50px 20px;
}

.card {
  background: white;
  width: 100%;
  max-width: 800px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.header {
  border-bottom: 2px solid #f0f2f5;
  margin-bottom: 25px;
  padding-bottom: 10px;
}

.header h1 {
  margin: 0;
  color: #007bff;
  font-size: 1.8rem;
}

.header p {
  color: #65676b;
  margin: 5px 0 0 0;
}

.form-section {
  margin-bottom: 30px;
}

.input-group {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #dddfe2;
  border-radius: 6px;
  font-size: 14px;
  transition: border 0.2s;
}

input:focus {
  outline: none;
  border-color: #007bff;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.btn-danger:hover {
  background-color: #d9363e;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
}

.styled-table th {
  text-align: left;
  background-color: #f8f9fa;
  padding: 12px;
  color: #4b4f56;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.styled-table td {
  padding: 15px 12px;
  border-bottom: 1px solid #f0f2f5;
  font-size: 15px;
}

.font-bold { font-weight: 600; }
.text-center { text-align: center; }
.muted { color: #8e8e8e; }
</style>