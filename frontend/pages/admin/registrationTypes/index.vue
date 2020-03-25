<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-registrationTypes.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onAdd)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-registrationTypes.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="eventRegistrationTypeName"
                :label="$t('forms.labels.eventRegistrationTypeName')"
                rules="required"
              />
              <e-input
                v-model="form.nameInEnglish"
                name="eventRegistrationTypeNameInEnglish"
                :label="$t('forms.labels.eventRegistrationTypeNameInEnglish')"
                rules="required"
              />

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary"
                    native-type="submit"
                    icon-left="plus"
                    :loading="loading"
                    >{{
                      $t('pages.admin-registrationTypes.addButton')
                    }}</b-button
                  >
                </div>
              </div>
            </form>
          </ValidationObserver>
          <div class="section">
            <b-table :data="registrationTypes" default-sort="name">
              <template v-slot="{ row }">
                <b-table-column
                  field="name"
                  :label="$t('pages.admin-registrationTypes.labels.name')"
                  sortable
                >
                  {{ row.name }}
                </b-table-column>
                <b-table-column
                  field="name_english"
                  :label="
                    $t('pages.admin-registrationTypes.labels.nameInEnglish')
                  "
                  sortable
                >
                  {{ row.name_english }}
                </b-table-column>
                <b-table-column
                  :label="$t('pages.admin-registrationTypes.labels.actions')"
                  width="200"
                  numeric
                >
                  <b-button
                    tag="nuxt-link"
                    :to="
                      localePath({
                        name: 'admin-registrationTypes-id',
                        params: {
                          id: row.id
                        }
                      })
                    "
                    >{{
                      $t('pages.admin-registrationTypes.editButton')
                    }}</b-button
                  >
                  <b-button type="is-danger" @click="onDelete(row.id)">{{
                    $t('pages.admin-registrationTypes.deleteButton')
                  }}</b-button>
                </b-table-column>
              </template>
            </b-table>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  data() {
    return {
      loading: false,
      error: null,
      form: {
        name: null,
        nameInEnglish: null
      }
    }
  },
  computed: {
    registrationTypes() {
      return this.$store.state.event.registration_types
    }
  },
  methods: {
    clearForm() {
      this.form.name = null
      this.form.nameInEnglish = null
      this.$refs.form.reset()
    },
    onAdd() {
      this.loading = true
      this.$store
        .dispatch('admin/addEventRegistrationType', this.form)
        .catch(this.handleError)
        .then(this.clearForm())
        .finally(() => {
          this.loading = false
        })
    },
    onDelete(registrationTypeId) {
      this.$store
        .dispatch('admin/deleteEventRegistrationType', registrationTypeId)
        .catch(this.handleErrorToast)
    },
    handleError(error) {
      switch (error.name) {
        case 'APIValidationError':
          this.error = error.message || this.$t('genericErrors.formValidation')
          this.$refs.form.setErrors(error.fields)
          break
        case 'APIError':
          this.error = this.$t('genericErrors.api')
          break
        default:
          this.error = this.$t('genericErrors.network')
      }
    },
    handleErrorToast(error) {
      let toastMessage = this.$t('genericErrors.network')
      switch (error.name) {
        case 'APIValidationError':
          toastMessage =
            error.message || this.$t('genericErrors.formValidation')
          break
        case 'APIError':
          toastMessage = this.$t('genericErrors.api')
          break
        default:
          toastMessage = this.$t('genericErrors.network')
      }
      this.$buefy.toast.open({
        message: toastMessage,
        position: 'is-bottom-right',
        duration: 10000,
        type: 'is-danger'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.registration-type {
  margin-bottom: 1em;
}
.registration-type .card-footer-item {
  padding: 0;
}
.registration-type .button {
  width: 100%;
  height: 100%;
  border-radius: 0;
  border: none;
}
</style>
