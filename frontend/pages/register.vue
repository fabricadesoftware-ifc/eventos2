<template>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-5">
        <main class="section">
          <h1 class="title">{{ $t('pages.register.title') }}</h1>
          <form @submit.prevent="onSubmit">
            <div v-visible="!loading" class="field">
              <b-message v-if="error" type="is-danger">
                {{ error }}
              </b-message>
              <b-message v-else type="is-info">
                {{ $t('pages.register.description') }}
              </b-message>
            </div>
            <div class="field">
              <e-radio-card
                v-for="registrationType in eventRegistrationTypes"
                :key="registrationType.id"
                v-model="form.registrationType"
                name="registrationType"
                :value="registrationType"
              >
                {{ registrationType.name }}
              </e-radio-card>
            </div>
            <div class="field">
              <div class="control">
                <b-button type="is-primary is-fullwidth" native-type="submit">
                  {{ $t('pages.register.submitButton') }}
                </b-button>
              </div>
            </div>
          </form>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ERadioCard from '~/components/ERadioCard'

export default {
  components: {
    ERadioCard
  },
  async fetch({ store }) {
    await store.dispatch('fetchEventRegistration')
  },
  data() {
    return {
      loading: false,
      error: null,
      form: {
        registrationType: null
      }
    }
  },
  computed: {
    ...mapGetters(['eventRegistrationTypes', 'eventUserRegistration'])
  },
  mounted() {
    if (this.eventUserRegistration) {
      this.$router.push(this.localePath({ name: 'index' }))
    }
  },
  methods: {
    onSubmit() {
      if (this.form.registrationType === null) {
        this.error = this.$t('pages.register.registrationTypeError')
        return
      }
      this.loading = true
      this.$store
        .dispatch('createEventRegistration', this.form.registrationType.id)
        .then(() => {
          this.$router.push(this.localePath({ name: 'index' }))
        })
        .catch(this.handleError)
        .finally(() => (this.loading = false))
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
    }
  }
}
</script>

<style lang="scss" scoped></style>
