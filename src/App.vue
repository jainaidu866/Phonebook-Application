<template>
  <div class="app-container">
    <div class="card">
      <header>
        <h1>Phonebook App</h1>
        <p class="subtitle">Professional Contact Management</p>
      </header>

      <div class="form-group">
        <input v-model="newContact.name" placeholder="Full Name" type="text" />
        <input v-model="newContact.phone" placeholder="Phone (+1234567890)" type="text" />
        <button class="add-btn" @click="addContact">Add Contact</button>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th style="text-align: right;">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contact in contacts" :key="contact.id">
              <td class="name-cell">{{ contact.name }}</td>
              <td class="phone-cell">{{ contact.phone }}</td>
              <td class="actions-cell">
                <button class="edit-btn" @click="openEditModal(contact)">Edit</button>
                <button class="delete-btn" @click="deleteContact(contact.id)">Delete</button>
              </td>
            </tr>
            <tr v-if="contacts.length === 0">
              <td colspan="3" class="empty-state">No contacts found. Run seed.py to add 50 contacts.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-card">
        <h3>Edit Contact</h3>
        <input v-model="editContactData.name" placeholder="Name" type="text" />
        <input v-model="editContactData.phone" placeholder="Phone" type="text" />
        <div class="modal-actions">
          <button class="save-btn" @click="updateContact">Save</button>
          <button class="cancel-btn" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 🔥 UPDATE this to your active Ngrok URL
const API_BASE = "https://staleness-gratified-alright.ngrok-free.dev";

const contacts = ref([]);
const showModal = ref(false);
const newContact = ref({ name: '', phone: '' });
const editContactData = ref({});

const fetchContacts = async () => {
  try {
    const response = await axios.get(`${API_BASE}/contacts`);
    contacts.value = response.data;
  } catch (error) { console.error(error); }
};

const addContact = async () => {
  try {
    await axios.post(`${API_BASE}/contacts`, newContact.value);
    newContact.value = { name: '', phone: '' };
    fetchContacts();
  } catch (error) { alert("Format Error! Use +1234567890"); }
};

const openEditModal = (c) => { editContactData.value = { ...c }; showModal.value = true; };

const updateContact = async () => {
  await axios.put(`${API_BASE}/contacts/${editContactData.value.id}`, editContactData.value);
  showModal.value = false;
  fetchContacts();
};

const deleteContact = async (id) => {
  if (confirm("Delete?")) { await axios.delete(`${API_BASE}/contacts/${id}`); fetchContacts(); }
};

onMounted(fetchContacts);
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
body { font-family: 'Inter', sans-serif; background: #f1f5f9; padding: 40px 20px; }
.card { background: white; max-width: 850px; margin: auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
header h1 { color: #2563eb; margin: 0; }
.subtitle { color: #64748b; margin-bottom: 25px; }
.form-group { display: flex; gap: 10px; margin-bottom: 30px; }
input { flex: 1; padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px; }
.add-btn { background: #2563eb; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: 600; cursor: pointer; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 12px; border-bottom: 2px solid #f1f5f9; color: #64748b; }
td { padding: 12px; border-bottom: 1px solid #f1f5f9; }
.name-cell { font-weight: 500; }
.actions-cell { text-align: right; }
.edit-btn { color: #059669; background: none; border: none; cursor: pointer; margin-right: 10px; }
.delete-btn { color: #dc2626; background: none; border: none; cursor: pointer; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal-card { background: white; padding: 30px; border-radius: 10px; width: 400px; display: flex; flex-direction: column; gap: 15px; }
.save-btn { background: #2563eb; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
</style>