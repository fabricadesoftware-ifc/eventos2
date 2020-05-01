<template>
  <div class="container">
    <div class="columns is-gapless">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ $t('pages.admin-registrations.title') }}</h1>
          <b-table
            :data="registrations"
            :columns="registrationColumns"
            default-sort="user.fullName"
          />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  fetch({ store }) {
    return store.dispatch('admin/fetchRegistrations')
  },
  computed: {
    registrationColumns() {
      return [
        {
          field: 'user.fullName',
          label: this.$t('pages.admin-registrations.labels.name'),
          sortable: true
        },
        {
          field: 'user.email',
          label: this.$t('pages.admin-registrations.labels.email'),
          sortable: true
        }
      ]
    },
    registrations() {
      return this.$store.getters['admin/registrations'].map(registration => ({
        user: {
          fullName:
            registration.user.first_name + ' ' + registration.user.last_name,
          ...registration.user
        }
      }))
    }
  }
}
</script>
