<template>
  <div class="app-container">
    <div class="card">
      <header class="header">
        <h1>Phonebook App</h1>
        <p>Manage your professional contacts efficiently.</p>
      </header>

      <section class="form-section">
        <div class="input-group">
          <input v-model="form.name" placeholder="Name" required />
          <input v-model="form.phone_number" placeholder="Phone (+1234567890)" required />
          <button @click="submitContact" class="btn-primary">Add Contact</button>
        </div>
        <p v-if="formError" class="error-msg">{{ formError }}</p>
      </section>

      <section class="list-section">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contact in contacts" :key="contact.id">
              <td class="font-bold">{{ contact.name }}</td>
              <td>{{ contact.phone_number }}</td>
              <td class="text-center">
                <button @click="openEdit(contact)" class="btn-edit">Edit</button>
                <button @click="deleteContact(contact.id)" class="btn-danger">Delete</button>
              </td>
            </tr>
            <tr v-if="contacts.length === 0">
              <td colspan="3" class="text-center muted">No contacts found.</td>
            </tr>
          </tbody>
        </table>
      </section>

      <div v-if="editModal" class="modal-overlay">
        <div class="modal">
          <h2>Edit Contact</h2>
          <div class="modal-form">
            <label>Name</label>
            <input v-model="editForm.name" />
            <label>Phone Number</label>
            <input v-model="editForm.phone_number" />
            <label>Email</label>
            <input v-model="editForm.email" />
            <label>Address</label>
            <input v-model="editForm.address" />
          </div>
          <p v-if="editError" class="error-msg">{{ editError }}</p>
          <div class="modal-actions">
            <button @click="updateContact" class="btn-primary">Save Changes</button>
            <button @click="closeEdit" class="btn-cancel">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const contacts = ref([])
const form = ref({ name: '', phone_number: '' })
const formError = ref('')
const editModal = ref(false)
const editForm = ref({})
const editError = ref('')
const editId = ref(null)

const isValidPhone = (phone) => /^\+?[1-9]\d{6,14}$/.test(phone)

const getContacts = async () => {
  const response = await axios.get('http://localhost:8000/contacts')
  contacts.value = response.data
}

const submitContact = async () => {
  formError.value = ''
  if (!form.value.name || !form.value.phone_number) {
    formError.value = 'Required fields missing.'
    return
  }
  if (!isValidPhone(form.value.phone_number)) {
    formError.value = 'Use format: +1234567890'
    return
  }
  try {
    await axios.post('http://localhost:8000/contacts', form.value)
    form.value = { name: '', phone_number: '' }
    getContacts()
  } catch (e) { formError.value = "Error saving contact." }
}

const openEdit = (contact) => {
  editId.value = contact.id
  editForm.value = { ...contact }
  editModal.value = true
}

const closeEdit = () => { editModal.value = false }

const updateContact = async () => {
  if (!isValidPhone(editForm.value.phone_number)) {
    editError.value = 'Invalid phone format.'
    return
  }
  await axios.put(`http://localhost:8000/contacts/${editId.value}`, editForm.value)
  editModal.value = false
  getContacts()
}

const deleteContact = async (id) => {
  if(confirm("Delete this contact?")) {
    await axios.delete(`http://localhost:8000/contacts/${id}`)
    getContacts()
  }
}

onMounted(getContacts)
</script>

<style scoped>
/* Same professional styles as before, adding Edit button and Modal styles */
:global(body) { background-color: #f0f2f5; margin: 0; color: #1c1e21; }
.app-container { display: flex; justify-content: center; padding: 50px 20px; }
.card { background: white; width: 100%; max-width: 800px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 30px; }
.header { border-bottom: 2px solid #f0f2f5; margin-bottom: 25px; padding-bottom: 10px; }
.header h1 { margin: 0; color: #007bff; font-size: 1.8rem; }
.input-group { display: flex; gap: 10px; }
input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; }
.btn-primary { background: #007bff; color: white; border: none; padding: 0 20px; border-radius: 6px; cursor: pointer; }
.btn-edit { background: #28a745; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; margin-right: 5px; }
.btn-danger { background: #ff4d4f; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.styled-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
.styled-table th, .styled-table td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
.text-center { text-align: center; }
.error-msg { color: #ff4d4f; font-size: 12px; margin-top: 5px; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: white; padding: 30px; border-radius: 12px; width: 400px; }
.modal-form { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.modal-form label { font-size: 12px; font-weight: bold; }
.modal-actions { margin-top: 20px; display: flex; gap: 10px; }
.btn-cancel { background: #6c757d; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
</style>