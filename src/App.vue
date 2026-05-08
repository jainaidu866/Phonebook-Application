<template>
  <div id="app">
    <!-- Animated background orbs -->
    <div class="bg-orb orb1"></div>
    <div class="bg-orb orb2"></div>
    <div class="bg-orb orb3"></div>

    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <div class="logo-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <div>
            <span class="logo-text">Phonebook</span>
            <span class="logo-sub">Pro</span>
          </div>
        </div>
        <div class="header-right">
          <div class="contact-badge">
            <span class="badge-dot"></span>
            {{ totalContacts }} Contacts
          </div>
          <button class="btn btn-primary" @click="openModal('create')">
            <span class="plus-icon">+</span> Add Contact
          </button>
        </div>
      </div>
    </header>

    <!-- Search + Stats Bar -->
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Search by name or phone…"
          class="search-input"
          @input="onSearch"
        />
        <button v-if="search" class="clear-search" @click="clearSearch">✕</button>
      </div>
      <div class="pagination-info" v-if="totalContacts > 0">
        Showing {{ pageStart }}–{{ pageEnd }} of {{ totalContacts }}
      </div>
    </div>

    <!-- Main Content -->
    <main class="main">
      <!-- Loading -->
      <div v-if="loading" class="state-center">
        <div class="loader"></div>
        <p class="state-text">Loading contacts…</p>
      </div>

      <!-- Empty -->
      <div v-else-if="contacts.length === 0" class="state-center">
        <div class="empty-icon">📭</div>
        <p class="state-text" v-if="search">No results for "<em>{{ search }}</em>"</p>
        <p class="state-text" v-else>No contacts yet. Add your first one!</p>
      </div>

      <!-- Grid -->
      <div v-else class="contact-grid">
        <div
          v-for="(contact, i) in paginatedContacts"
          :key="contact.id"
          class="card"
          :style="{ animationDelay: `${i * 0.05}s` }"
        >
          <div class="card-top">
            <div class="avatar" :style="{ background: avatarGradient(contact.name) }">
              {{ initials(contact.name) }}
            </div>
            <div class="card-actions">
              <button class="icon-btn edit" @click="openModal('edit', contact)" title="Edit">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button class="icon-btn del" @click="confirmDelete(contact)" title="Delete">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
              </button>
            </div>
          </div>
          <h3 class="card-name">{{ contact.name }}</h3>
          <div class="card-detail">
            <span class="detail-icon">📞</span>
            <span>{{ contact.phone_number }}</span>
          </div>
          <div class="card-detail" v-if="contact.email">
            <span class="detail-icon">✉️</span>
            <span class="truncate">{{ contact.email }}</span>
          </div>
          <div class="card-detail" v-if="contact.address">
            <span class="detail-icon">📍</span>
            <span class="truncate">{{ contact.address }}</span>
          </div>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" @click="goToPage(1)" :disabled="currentPage === 1" title="First">«</button>
        <button class="page-btn" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" title="Previous">‹</button>

        <button
          v-for="p in visiblePages"
          :key="p"
          class="page-btn"
          :class="{ active: p === currentPage, ellipsis: p === '…' }"
          @click="p !== '…' && goToPage(p)"
        >{{ p }}</button>

        <button class="page-btn" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages" title="Next">›</button>
        <button class="page-btn" @click="goToPage(totalPages)" :disabled="currentPage === totalPages" title="Last">»</button>
      </div>
    </main>

    <!-- Add / Edit Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="modal.show" class="overlay" @click.self="closeModal">
          <div class="modal">
            <div class="modal-header">
              <h2>{{ modal.mode === 'create' ? '✨ New Contact' : '✏️ Edit Contact' }}</h2>
              <button class="close-btn" @click="closeModal">✕</button>
            </div>
            <div class="modal-body">
              <div class="field">
                <label>Full Name <span class="req">*</span></label>
                <input v-model="form.name" type="text" placeholder="e.g. Priya Patel" :class="{ err: errors.name }" />
                <span class="err-msg" v-if="errors.name">{{ errors.name }}</span>
              </div>
              <div class="field">
                <label>Phone Number <span class="req">*</span></label>
                <input v-model="form.phone_number" type="text" placeholder="+91 98765 43210" :class="{ err: errors.phone_number }" />
                <span class="err-msg" v-if="errors.phone_number">{{ errors.phone_number }}</span>
              </div>
              <div class="field">
                <label>Email <span class="optional">(optional)</span></label>
                <input v-model="form.email" type="email" placeholder="priya@example.com" :class="{ err: errors.email }" />
                <span class="err-msg" v-if="errors.email">{{ errors.email }}</span>
              </div>
              <div class="field">
                <label>Address <span class="optional">(optional)</span></label>
                <textarea v-model="form.address" placeholder="Street, City, State" rows="2"></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-ghost" @click="closeModal">Cancel</button>
              <button class="btn btn-primary" @click="submitForm" :disabled="submitting">
                <span v-if="submitting" class="btn-spinner"></span>
                {{ submitting ? 'Saving…' : modal.mode === 'create' ? 'Add Contact' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Delete Confirm Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="deleteTarget" class="overlay" @click.self="deleteTarget = null">
          <div class="modal confirm">
            <div class="confirm-icon">🗑️</div>
            <h2>Delete Contact?</h2>
            <p>You're about to delete <strong>{{ deleteTarget.name }}</strong>. This action cannot be undone.</p>
            <div class="modal-footer" style="justify-content:center; gap:12px;">
              <button class="btn btn-ghost" @click="deleteTarget = null">Cancel</button>
              <button class="btn btn-danger" @click="deleteContact" :disabled="submitting">
                {{ submitting ? 'Deleting…' : 'Yes, Delete' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        <span>{{ toast.type === 'success' ? '✅' : '❌' }}</span>
        {{ toast.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const PER_PAGE = 10

// ── State ──────────────────────────────────────────────────────────────────────
const allContacts  = ref([])
const search       = ref('')
const loading      = ref(false)
const submitting   = ref(false)
const currentPage  = ref(1)
const deleteTarget = ref(null)
const modal  = reactive({ show: false, mode: 'create', id: null })
const form   = reactive({ name: '', phone_number: '', email: '', address: '' })
const errors = reactive({ name: '', phone_number: '', email: '' })
const toast  = reactive({ show: false, message: '', type: 'success' })

// ── Computed ───────────────────────────────────────────────────────────────────
const contacts = computed(() => {
  if (!search.value.trim()) return allContacts.value
  const q = search.value.toLowerCase()
  return allContacts.value.filter(c =>
    c.name.toLowerCase().includes(q) || c.phone_number.includes(q)
  )
})

const totalContacts  = computed(() => contacts.value.length)
const totalPages     = computed(() => Math.ceil(totalContacts.value / PER_PAGE))
const pageStart      = computed(() => totalContacts.value === 0 ? 0 : (currentPage.value - 1) * PER_PAGE + 1)
const pageEnd        = computed(() => Math.min(currentPage.value * PER_PAGE, totalContacts.value))

const paginatedContacts = computed(() =>
  contacts.value.slice((currentPage.value - 1) * PER_PAGE, currentPage.value * PER_PAGE)
)

const visiblePages = computed(() => {
  const total = totalPages.value
  const cur   = currentPage.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages = []
  if (cur <= 4) {
    pages.push(1, 2, 3, 4, 5, '…', total)
  } else if (cur >= total - 3) {
    pages.push(1, '…', total-4, total-3, total-2, total-1, total)
  } else {
    pages.push(1, '…', cur-1, cur, cur+1, '…', total)
  }
  return pages
})

// ── Helpers ────────────────────────────────────────────────────────────────────
const GRADIENTS = [
  'linear-gradient(135deg,#667eea,#764ba2)',
  'linear-gradient(135deg,#f093fb,#f5576c)',
  'linear-gradient(135deg,#4facfe,#00f2fe)',
  'linear-gradient(135deg,#43e97b,#38f9d7)',
  'linear-gradient(135deg,#fa709a,#fee140)',
  'linear-gradient(135deg,#a18cd1,#fbc2eb)',
  'linear-gradient(135deg,#fccb90,#d57eeb)',
  'linear-gradient(135deg,#84fab0,#8fd3f4)',
]
function avatarGradient(name) {
  return GRADIENTS[name.charCodeAt(0) % GRADIENTS.length]
}
function initials(name) {
  return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
}
function showToast(message, type = 'success') {
  toast.message = message; toast.type = type; toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}
function resetErrors() { errors.name = ''; errors.phone_number = ''; errors.email = '' }

// ── Data ───────────────────────────────────────────────────────────────────────
async function fetchContacts() {
  loading.value = true
  try {
    const res = await axios.get(`${API}/contacts`)
    allContacts.value = res.data
  } catch {
    showToast('Failed to load contacts', 'error')
  } finally {
    loading.value = false
  }
}

function onSearch() { currentPage.value = 1 }
function clearSearch() { search.value = ''; currentPage.value = 1 }

// ── Pagination ─────────────────────────────────────────────────────────────────
function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── Modal ──────────────────────────────────────────────────────────────────────
function openModal(mode, contact = null) {
  modal.mode = mode; modal.show = true; resetErrors()
  if (mode === 'edit' && contact) {
    modal.id = contact.id
    form.name = contact.name; form.phone_number = contact.phone_number
    form.email = contact.email || ''; form.address = contact.address || ''
  } else {
    modal.id = null
    Object.assign(form, { name: '', phone_number: '', email: '', address: '' })
  }
}
function closeModal() { modal.show = false }

// ── Validation ─────────────────────────────────────────────────────────────────
function validate() {
  resetErrors(); let ok = true
  if (!form.name.trim())         { errors.name = 'Name is required'; ok = false }
  if (!form.phone_number.trim()) { errors.phone_number = 'Phone is required'; ok = false }
  else if (!/^\+?\d{7,15}$/.test(form.phone_number.replace(/[\s\-()\+]/g, '')))
                                 { errors.phone_number = 'Use format: +1234567890'; ok = false }
  if (form.email && !/^[^@]+@[^@]+\.[^@]+$/.test(form.email))
                                 { errors.email = 'Invalid email'; ok = false }
  return ok
}

// ── CRUD ───────────────────────────────────────────────────────────────────────
async function submitForm() {
  if (!validate()) return
  submitting.value = true
  const payload = {
    name: form.name.trim(), phone_number: form.phone_number.trim(),
    email: form.email.trim() || null, address: form.address.trim() || null,
  }
  try {
    if (modal.mode === 'create') {
      await axios.post(`${API}/contacts`, payload)
      showToast('Contact added successfully!')
    } else {
      await axios.put(`${API}/contacts/${modal.id}`, payload)
      showToast('Contact updated!')
    }
    closeModal(); await fetchContacts()
  } catch (e) {
    const d = e.response?.data?.detail
    if (d?.toLowerCase().includes('phone')) errors.phone_number = d
    else if (d?.toLowerCase().includes('email')) errors.email = d
    else showToast(d || 'Something went wrong', 'error')
  } finally { submitting.value = false }
}

function confirmDelete(contact) { deleteTarget.value = contact }
async function deleteContact() {
  submitting.value = true
  try {
    await axios.delete(`${API}/contacts/${deleteTarget.value.id}`)
    showToast('Contact deleted')
    deleteTarget.value = null; await fetchContacts()
    if (currentPage.value > totalPages.value) currentPage.value = Math.max(1, totalPages.value)
  } catch { showToast('Failed to delete', 'error') }
  finally { submitting.value = false }
}

onMounted(fetchContacts)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Clash+Display:wght@600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #080c14;
  --surface:    rgba(255,255,255,0.04);
  --glass:      rgba(255,255,255,0.07);
  --glass-b:    rgba(255,255,255,0.12);
  --border:     rgba(255,255,255,0.10);
  --border-h:   rgba(255,255,255,0.20);
  --text:       #f0f4ff;
  --muted:      rgba(255,255,255,0.45);
  --accent:     #6c63ff;
  --accent2:    #00d4ff;
  --danger:     #ff4d6d;
  --success:    #00e5a0;
  --radius:     18px;
  --font:       'Outfit', sans-serif;
  --font-head:  'Outfit', sans-serif;
}

html { scroll-behavior: smooth; }

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Background Orbs ────────────────────────────────────────── */
.bg-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.18;
  pointer-events: none;
  z-index: 0;
  animation: drift 12s ease-in-out infinite alternate;
}
.orb1 { width: 500px; height: 500px; background: #6c63ff; top: -150px; left: -100px; animation-delay: 0s; }
.orb2 { width: 400px; height: 400px; background: #00d4ff; bottom: -100px; right: -100px; animation-delay: -4s; }
.orb3 { width: 300px; height: 300px; background: #f093fb; top: 40%; left: 40%; animation-delay: -8s; }
@keyframes drift {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(30px, 20px) scale(1.05); }
}

/* ── Header ─────────────────────────────────────────────────── */
.header {
  position: sticky; top: 0; z-index: 100;
  background: rgba(8,12,20,0.75);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  max-width: 1200px; margin: 0 auto;
  padding: 16px 28px;
  display: flex; align-items: center; justify-content: space-between;
}
.logo { display: flex; align-items: center; gap: 12px; }
.logo-icon {
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex; align-items: center; justify-content: center;
  color: #fff; box-shadow: 0 0 20px rgba(108,99,255,0.4);
}
.logo-text {
  font-family: var(--font-head); font-size: 22px; font-weight: 800;
  background: linear-gradient(135deg, #fff, var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.logo-sub {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--accent2); text-transform: uppercase;
  display: block; margin-top: -4px;
}
.header-right { display: flex; align-items: center; gap: 14px; }
.contact-badge {
  display: flex; align-items: center; gap: 7px;
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 30px; padding: 6px 14px;
  font-size: 13px; font-weight: 500; color: var(--muted);
}
.badge-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 8px var(--success);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Buttons ─────────────────────────────────────────────────── */
.btn {
  border: none; border-radius: 12px; cursor: pointer;
  font-family: var(--font); font-size: 14px; font-weight: 600;
  padding: 11px 22px; transition: all 0.2s; display: inline-flex; align-items: center; gap: 7px;
}
.btn:active { transform: scale(0.96); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary {
  background: linear-gradient(135deg, var(--accent), #8b5cf6);
  color: #fff;
  box-shadow: 0 4px 20px rgba(108,99,255,0.4);
}
.btn-primary:hover:not(:disabled) {
  box-shadow: 0 6px 28px rgba(108,99,255,0.6);
  transform: translateY(-1px);
}
.btn-ghost {
  background: var(--glass); border: 1px solid var(--border); color: var(--text);
}
.btn-ghost:hover { background: var(--glass-b); border-color: var(--border-h); }
.btn-danger {
  background: linear-gradient(135deg, var(--danger), #ff6b35);
  color: #fff; box-shadow: 0 4px 16px rgba(255,77,109,0.35);
}
.btn-danger:hover:not(:disabled) { box-shadow: 0 6px 24px rgba(255,77,109,0.55); transform: translateY(-1px); }
.plus-icon { font-size: 20px; line-height: 1; }
.btn-spinner {
  width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: inline-block;
}

/* ── Toolbar ─────────────────────────────────────────────────── */
.toolbar {
  max-width: 1200px; margin: 28px auto 0; padding: 0 28px;
  display: flex; align-items: center; gap: 20px;
  position: relative; z-index: 1;
}
.search-wrap {
  flex: 1; display: flex; align-items: center; gap: 10px;
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 14px; padding: 0 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.search-wrap:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(108,99,255,0.15);
}
.search-svg { color: var(--muted); flex-shrink: 0; }
.search-input {
  flex: 1; border: none; outline: none; background: transparent;
  font-family: var(--font); font-size: 15px; color: var(--text);
  padding: 13px 0;
}
.search-input::placeholder { color: var(--muted); }
.clear-search {
  background: none; border: none; cursor: pointer;
  color: var(--muted); font-size: 13px; padding: 3px 5px;
  border-radius: 6px; transition: color 0.15s;
}
.clear-search:hover { color: var(--text); }
.pagination-info {
  font-size: 13px; color: var(--muted); white-space: nowrap;
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 10px; padding: 8px 14px;
}

/* ── Main ────────────────────────────────────────────────────── */
.main {
  max-width: 1200px; margin: 24px auto 60px;
  padding: 0 28px; position: relative; z-index: 1;
}

/* ── State ───────────────────────────────────────────────────── */
.state-center { text-align: center; padding: 80px 0; }
.state-text { color: var(--muted); margin-top: 16px; font-size: 15px; }
.state-text em { color: var(--accent2); font-style: normal; font-weight: 600; }
.empty-icon { font-size: 52px; }
.loader {
  width: 40px; height: 40px; border: 3px solid var(--glass-b);
  border-top-color: var(--accent); border-radius: 50%;
  animation: spin 0.8s linear infinite; margin: 0 auto;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Contact Grid ────────────────────────────────────────────── */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 18px;
}

/* ── Card ────────────────────────────────────────────────────── */
.card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  backdrop-filter: blur(12px);
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  animation: fadeUp 0.4s ease both;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(108,99,255,0.03), rgba(0,212,255,0.03));
  opacity: 0; transition: opacity 0.3s;
}
.card:hover { transform: translateY(-4px); border-color: var(--border-h); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
.card:hover::before { opacity: 1; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
.card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.avatar {
  width: 50px; height: 50px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 17px; color: #fff;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  letter-spacing: 0.5px;
}
.card-actions { display: flex; gap: 8px; }
.icon-btn {
  width: 34px; height: 34px; border-radius: 10px; border: 1px solid var(--border);
  background: var(--surface); cursor: pointer; color: var(--muted);
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.icon-btn.edit:hover  { background: rgba(108,99,255,0.15); border-color: var(--accent); color: var(--accent); }
.icon-btn.del:hover   { background: rgba(255,77,109,0.15); border-color: var(--danger); color: var(--danger); }
.card-name {
  font-size: 16px; font-weight: 700; margin-bottom: 10px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.card-detail {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: var(--muted); margin-top: 5px;
}
.detail-icon { font-size: 14px; flex-shrink: 0; }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Pagination ───────────────────────────────────────────────── */
.pagination {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; margin-top: 40px;
}
.page-btn {
  width: 40px; height: 40px; border-radius: 11px;
  border: 1px solid var(--border); background: var(--glass);
  color: var(--muted); cursor: pointer; font-family: var(--font);
  font-size: 14px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s; backdrop-filter: blur(8px);
}
.page-btn:hover:not(:disabled):not(.ellipsis) {
  border-color: var(--accent); color: var(--accent);
  background: rgba(108,99,255,0.12);
}
.page-btn.active {
  background: linear-gradient(135deg, var(--accent), #8b5cf6);
  border-color: transparent; color: #fff;
  box-shadow: 0 4px 16px rgba(108,99,255,0.4);
}
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.page-btn.ellipsis { cursor: default; border-color: transparent; background: transparent; }

/* ── Modal ────────────────────────────────────────────────────── */
.overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(4,6,12,0.7);
  backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
}
.modal {
  background: rgba(12,16,28,0.95);
  border: 1px solid var(--border-h);
  border-radius: 22px; width: 100%; max-width: 460px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(108,99,255,0.1);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24px 26px 0;
}
.modal-header h2 { font-size: 20px; font-weight: 800; }
.close-btn {
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 8px; width: 32px; height: 32px;
  cursor: pointer; color: var(--muted); font-size: 14px;
  display: flex; align-items: center; justify-content: center;
}
.close-btn:hover { color: var(--text); background: var(--glass-b); }
.modal-body { padding: 22px 26px; display: flex; flex-direction: column; gap: 18px; }
.modal-footer { padding: 0 26px 24px; display: flex; justify-content: flex-end; gap: 10px; }

.confirm { padding: 36px 28px; text-align: center; }
.confirm-icon { font-size: 44px; margin-bottom: 16px; }
.confirm h2 { font-size: 20px; font-weight: 800; margin-bottom: 10px; }
.confirm p { color: var(--muted); line-height: 1.6; margin-bottom: 24px; }

/* ── Form Fields ─────────────────────────────────────────────── */
.field { display: flex; flex-direction: column; gap: 7px; }
.field label { font-size: 13px; font-weight: 600; color: var(--muted); letter-spacing: 0.3px; }
.req { color: var(--danger); }
.optional { font-weight: 400; opacity: 0.6; }
.field input, .field textarea {
  background: var(--glass); border: 1.5px solid var(--border);
  border-radius: 12px; padding: 11px 14px;
  font-family: var(--font); font-size: 14px; color: var(--text);
  outline: none; transition: border-color 0.2s, box-shadow 0.2s;
  resize: vertical;
}
.field input::placeholder, .field textarea::placeholder { color: var(--muted); }
.field input:focus, .field textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(108,99,255,0.15);
}
.field input.err { border-color: var(--danger); }
.err-msg { font-size: 12px; color: var(--danger); }

/* ── Toast ────────────────────────────────────────────────────── */
.toast {
  position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%);
  padding: 13px 22px; border-radius: 12px;
  font-weight: 600; font-size: 14px; z-index: 2000;
  display: flex; align-items: center; gap: 9px;
  backdrop-filter: blur(10px); white-space: nowrap;
  box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.toast.success { background: rgba(0,229,160,0.15); border: 1px solid rgba(0,229,160,0.35); color: var(--success); }
.toast.error   { background: rgba(255,77,109,0.15); border: 1px solid rgba(255,77,109,0.35); color: var(--danger); }

/* ── Transitions ─────────────────────────────────────────────── */
.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-from { opacity: 0; transform: scale(0.94) translateY(10px); }
.modal-leave-to   { opacity: 0; transform: scale(0.94) translateY(10px); }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translate(-50%, 12px); }
.toast-leave-to   { opacity: 0; transform: translate(-50%, 12px); }

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 640px) {
  .header-inner { padding: 14px 16px; }
  .logo-sub { display: none; }
  .contact-badge { display: none; }
  .toolbar, .main { padding: 0 16px; }
  .contact-grid { grid-template-columns: 1fr; }
  .page-btn { width: 36px; height: 36px; font-size: 13px; }
}
</style>