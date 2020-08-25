<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-activities-new.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-activities-new.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.activityName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.activityNameInEnglish')"
                rules="required"
              />
              <e-input
                v-model="form.slug"
                name="slug"
                :label="$t('forms.labels.activitySlug')"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.activityStartDate')"
              ></e-datetimepicker>
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.activityEndDate')"
              ></e-datetimepicker>

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="plus"
                    :loading="loading"
                    >{{
                      $t('pages.admin-activities-new.submitButton')
                    }}</b-button
                  >
                </div>
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
  layout: 'admin',
  mixins: [errorMixin],

  data() {
    return {
      loading: false,
      error: null,
      form: {
        name: '',
        name_english: '',
        slug: '',
        starts_on: new Date(),
        ends_on: new Date()
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.activity
        .create({ eventSlug: this.$store.state.event.slug, ...this.form })
        .then(() =>
          this.$router.push(this.localePath({ name: 'admin-activities' }))
        )
        .catch(this.handleGenericError)
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>
