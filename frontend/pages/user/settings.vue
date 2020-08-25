<template>
  <div class="container">
    <div class="columns is-gapless is-centered">
      <div class="column is-8">
        <main class="section">
          <h1 class="title">{{ $t('pages.user-settings.title') }}</h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
              </div>
              <e-input
                v-model="form.first_name"
                name="first_name"
                :label="$t('forms.labels.firstName')"
                rules="required"
                horizontal
              />
              <e-input
                v-model="form.last_name"
                name="last_name"
                :label="$t('forms.labels.lastName')"
                rules="required"
                horizontal
              />
              <div class="field is-horizontal">
                <div class="field-label"></div>
                <div class="field-body">
                  <div class="field">
                    <b-button
                      type="is-primary is-fullwidth"
                      native-type="submit"
                      icon-left="wrench"
                      :loading="loading"
                      >{{ $t('pages.user-settings.submitButton') }}</b-button
                    >
                  </div>
                </div>
                <div class="control"></div>
              </div>
            </form>
          </ValidationObserver>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import errorMixin from '~/mixins/errorMixin'

export default {
  mixins: [errorMixin],

  data() {
    return {
      loading: false,
      form: {
        first_name: '',
        last_name: ''
      }
    }
  },
  created() {
    this.form = {
      first_name: this.$auth.user.first_name,
      last_name: this.$auth.user.last_name
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.user
        .update(this.form)
        .then(() => this.$auth.fetchUser())
        .catch(this.handleGenericError)
        .finally(() => (this.loading = false))
    }
  }
}
</script>
