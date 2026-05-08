<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">📒</span>
          <span class="logo-text">Phonebook</span>
        </div>
        <button class="btn btn-primary" @click="openModal('create')">
          <span class="btn-icon">+</span> Add Contact
        </button>
      </div>
    </header>

    <!-- Search Bar -->
    <div class="search-bar-wrap">
      <div class="search-bar">
        <span class="search-icon">🔍</span>
        <input
          v-model="search"
          type="text"
          placeholder="Search by name or phone…"
          class="search-input"
          @input="fetchContacts"
        />
        <button v-if="search" class="clear-btn" @click="clearSearch">✕</button>
      </div>
      <p class="result-count">
        {{ contacts.length }} contact{{ contacts.length !== 1 ? 's' : '' }}
        <span v-if="search"> matching "<em>{{ search }}</em>"</span>
      </p>
    </div>

    <!-- Contact Grid -->
    <main class="main">
      <div v-if="loading" class="empty-state">
        <div class="spinner"></div>
        <p>Loading contacts…</p>
      </div>

      <div v-else-if="contacts.length === 0" class="empty-state">
        <span class="empty-icon">📭</span>
        <p v-if="search">No contacts found for "{{ search }}"</p>
        <p v-else>No contacts yet. Add your first one!</p>
      </div>

      <div v-else class="contact-grid">
        <div
          v-for="contact in contacts"
          :key="contact.id"
          class="contact-card"
        >
          <div class="contact-avatar" :style="{ background: avatarColor(contact.name) }">
            {{ initials(contact.name) }}
          </div>
          <div class="contact-info">
            <h3 class="contact-name">{{ contact.name }}</h3>
            <p class="contact-phone">📞 {{ contact.phone_number }}</p>
            <p v-if="contact.email" class="contact-email">✉️ {{ contact.email }}</p>
            <p v-if="contact.address" class="contact-address">📍 {{ contact.address }}</p>
          </div>
          <div class="contact-actions">
            <button class="action-btn edit-btn" @click="openModal('edit', contact)" title="Edit">✏️</button>
            <button class="action-btn del-btn" @click="confirmDelete(contact)" title="Delete">🗑️</button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="modal.show" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <h2>{{ modal.mode === 'create' ? 'New Contact' : 'Edit Contact' }}</h2>
            <button class="close-btn" @click="closeModal">✕</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Name <span class="required">*</span></label>
              <input v-model="form.name" type="text" placeholder="Full name" :class="{ error: errors.name }" />
              <span class="err-msg" v-if="errors.name">{{ errors.name }}</span>
            </div>
            <div class="form-group">
              <label>Phone <span class="required">*</span></label>
              <input v-model="form.phone_number" type="text" placeholder="+1234567890" :class="{ error: errors.phone_number }" />
              <span class="err-msg" v-if="errors.phone_number">{{ errors.phone_number }}</span>
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="form.email" type="email" placeholder="email@example.com" :class="{ error: errors.email }" />
              <span class="err-msg" v-if="errors.email">{{ errors.email }}</span>
            </div>
            <div class="form-group">
              <label>Address</label>
              <textarea v-model="form.address" placeholder="Street, City, State" rows="2"></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-ghost" @click="closeModal">Cancel</button>
            <button class="btn btn-primary" @click="submitForm" :disabled="submitting">
              {{ submitting ? 'Saving…' : (modal.mode === 'create' ? 'Add Contact' : 'Save Changes') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirm -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
        <div class="modal confirm-modal">
          <h2>Delete Contact?</h2>
          <p>Are you sure you want to delete <strong>{{ deleteTarget.name }}</strong>? This cannot be undone.</p>
          <div class="modal-footer">
            <button class="btn btn-ghost" @click="deleteTarget = null">Cancel</button>
            <button class="btn btn-danger" @click="deleteContact" :disabled="submitting">
              {{ submitting ? 'Deleting…' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast -->
    <div v-if="toast.show" :class="['toast', toast.type]">{{ toast.message }}</div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const contacts = ref([])
const search   = ref('')
const loading  = ref(false)
const submitting = ref(false)
const deleteTarget = ref(null)

const modal = reactive({ show: false, mode: 'create', id: null })
const form  = reactive({ name: '', phone_number: '', email: '', address: '' })
const errors = reactive({ name: '', phone_number: '', email: '' })
const toast  = reactive({ show: false, message: '', type: 'success' })

// ── Helpers ──────────────────────────────────────────────────────────────────

function initials(name) {
  return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
}

const COLORS = ['#4f7cff','#ff6b6b','#f7b731','#26de81','#fd9644','#a55eea','#2bcbba','#fc5c65']
function avatarColor(name) {
  const idx = name.charCodeAt(0) % COLORS.length
  return COLORS[idx]
}

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// ── Data ─────────────────────────────────────────────────────────────────────

async function fetchContacts() {
  loading.value = true
  try {
    const params = search.value ? { search: search.value } : {}
    const res = await axios.get(`${API}/contacts`, { params })
    contacts.value = res.data
  } catch {
    showToast('Failed to load contacts', 'error')
  } finally {
    loading.value = false
  }
}

function clearSearch() {
  search.value = ''
  fetchContacts()
}

// ── Modal ─────────────────────────────────────────────────────────────────────

function openModal(mode, contact = null) {
  modal.mode = mode
  modal.show = true
  resetErrors()
  if (mode === 'edit' && contact) {
    modal.id = contact.id
    form.name = contact.name
    form.phone_number = contact.phone_number
    form.email = contact.email || ''
    form.address = contact.address || ''
  } else {
    modal.id = null
    Object.assign(form, { name: '', phone_number: '', email: '', address: '' })
  }
}

function closeModal() {
  modal.show = false
}

function resetErrors() {
  errors.name = ''
  errors.phone_number = ''
  errors.email = ''
}

// ── Validation ────────────────────────────────────────────────────────────────

function validate() {
  resetErrors()
  let valid = true
  if (!form.name.trim()) { errors.name = 'Name is required'; valid = false }
  if (!form.phone_number.trim()) {
    errors.phone_number = 'Phone number is required'; valid = false
  } else if (!/^\+?\d{7,15}$/.test(form.phone_number.replace(/[\s\-()]/g, ''))) {
    errors.phone_number = 'Invalid format (e.g. +1234567890)'; valid = false
  }
  if (form.email && !/^[^@]+@[^@]+\.[^@]+$/.test(form.email)) {
    errors.email = 'Invalid email format'; valid = false
  }
  return valid
}

// ── CRUD ──────────────────────────────────────────────────────────────────────

async function submitForm() {
  if (!validate()) return
  submitting.value = true
  const payload = {
    name: form.name.trim(),
    phone_number: form.phone_number.trim(),
    email: form.email.trim() || null,
    address: form.address.trim() || null,
  }
  try {
    if (modal.mode === 'create') {
      await axios.post(`${API}/contacts`, payload)
      showToast('Contact added!')
    } else {
      await axios.put(`${API}/contacts/${modal.id}`, payload)
      showToast('Contact updated!')
    }
    closeModal()
    fetchContacts()
  } catch (err) {
    const detail = err.response?.data?.detail
    if (detail?.includes('phone')) errors.phone_number = detail
    else if (detail?.includes('email')) errors.email = detail
    else showToast(detail || 'An error occurred', 'error')
  } finally {
    submitting.value = false
  }
}

function confirmDelete(contact) {
  deleteTarget.value = contact
}

async function deleteContact() {
  submitting.value = true
  try {
    await axios.delete(`${API}/contacts/${deleteTarget.value.id}`)
    showToast('Contact deleted')
    deleteTarget.value = null
    fetchContacts()
  } catch {
    showToast('Failed to delete contact', 'error')
  } finally {
    submitting.value = false
  }
}

onMounted(fetchContacts)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #f4f5f9;
  --surface:  #ffffff;
  --border:   #e5e7ef;
  --text:     #1a1d2e;
  --muted:    #6b7280;
  --primary:  #4f46e5;
  --primary-h:#3730a3;
  --danger:   #ef4444;
  --success:  #10b981;
  --radius:   14px;
  --shadow:   0 2px 12px rgba(0,0,0,0.07);
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}

/* ── Header ────────────────────────────────────────────────── */
.header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo { display: flex; align-items: center; gap: 10px; }
.logo-icon { font-size: 26px; }
.logo-text { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: var(--primary); letter-spacing: -0.5px; }

/* ── Buttons ───────────────────────────────────────────────── */
.btn {
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 20px;
  transition: background 0.15s, opacity 0.15s, transform 0.1s;
}
.btn:active { transform: scale(0.97); }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background: var(--primary); color: #fff; display: flex; align-items: center; gap: 6px; }
.btn-primary:hover:not(:disabled) { background: var(--primary-h); }
.btn-ghost  { background: var(--bg); color: var(--text); }
.btn-ghost:hover { background: var(--border); }
.btn-danger { background: var(--danger); color: #fff; }
.btn-danger:hover:not(:disabled) { background: #dc2626; }
.btn-icon { font-size: 18px; line-height: 1; }

/* ── Search ────────────────────────────────────────────────── */
.search-bar-wrap {
  max-width: 1100px;
  margin: 28px auto 0;
  padding: 0 24px;
}
.search-bar {
  display: flex;
  align-items: center;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  padding: 0 14px;
  gap: 10px;
  transition: border-color 0.2s;
}
.search-bar:focus-within { border-color: var(--primary); }
.search-icon { font-size: 17px; color: var(--muted); }
.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-family: inherit;
  font-size: 15px;
  padding: 13px 0;
  background: transparent;
  color: var(--text);
}
.clear-btn { background: none; border: none; cursor: pointer; color: var(--muted); font-size: 14px; padding: 4px; }
.result-count { margin-top: 10px; font-size: 13px; color: var(--muted); }
.result-count em { color: var(--primary); font-style: normal; font-weight: 600; }

/* ── Main Grid ─────────────────────────────────────────────── */
.main {
  max-width: 1100px;
  margin: 24px auto 60px;
  padding: 0 24px;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

/* ── Contact Card ──────────────────────────────────────────── */
.contact-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  transition: box-shadow 0.2s, transform 0.2s;
}
.contact-card:hover { box-shadow: var(--shadow); transform: translateY(-2px); }

.contact-avatar {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: #fff;
  flex-shrink: 0;
}

.contact-info { flex: 1; min-width: 0; }
.contact-name { font-size: 15px; font-weight: 700; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.contact-phone, .contact-email, .contact-address {
  font-size: 13px;
  color: var(--muted);
  margin-top: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-actions { display: flex; flex-direction: column; gap: 6px; flex-shrink: 0; }
.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg);
  cursor: pointer;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}
.edit-btn:hover { background: #e0e7ff; }
.del-btn:hover  { background: #fee2e2; }

/* ── Empty / Loading ───────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 80px 0;
  color: var(--muted);
}
.empty-icon { font-size: 48px; display: block; margin-bottom: 12px; }
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Modal ─────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10,12,24,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
  padding: 20px;
}
.modal {
  background: var(--surface);
  border-radius: 18px;
  width: 100%;
  max-width: 460px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  animation: slideUp 0.2s ease;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 22px 24px 0;
}
.modal-header h2 { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; }
.close-btn { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--muted); padding: 4px; }
.modal-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; }
.modal-footer { padding: 0 24px 22px; display: flex; justify-content: flex-end; gap: 10px; }

.confirm-modal { padding: 28px 24px; text-align: center; }
.confirm-modal h2 { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 12px; }
.confirm-modal p { color: var(--muted); margin-bottom: 24px; line-height: 1.5; }
.confirm-modal .modal-footer { padding: 0; justify-content: center; }

/* ── Form ──────────────────────────────────────────────────── */
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: var(--muted); }
.required { color: var(--danger); }
.form-group input,
.form-group textarea {
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-family: inherit;
  font-size: 14px;
  padding: 10px 13px;
  outline: none;
  color: var(--text);
  transition: border-color 0.2s;
  resize: vertical;
}
.form-group input:focus,
.form-group textarea:focus { border-color: var(--primary); }
.form-group input.error { border-color: var(--danger); }
.err-msg { font-size: 12px; color: var(--danger); }

/* ── Toast ─────────────────────────────────────────────────── */
.toast {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  z-index: 2000;
  animation: fadeInUp 0.25s ease;
  white-space: nowrap;
}
.toast.success { background: var(--success); color: #fff; }
.toast.error   { background: var(--danger);  color: #fff; }
@keyframes fadeInUp {
  from { opacity: 0; transform: translate(-50%, 10px); }
  to   { opacity: 1; transform: translate(-50%, 0); }
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 600px) {
  .contact-grid { grid-template-columns: 1fr; }
  .header-inner { padding: 14px 16px; }
  .main, .search-bar-wrap { padding: 0 16px; }
}
</style>