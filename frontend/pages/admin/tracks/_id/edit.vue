<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-tracks-id-edit.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-tracks-id-edit.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.trackName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.trackNameInEnglish')"
                rules="required"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.trackStartDate')"
              />
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.trackEndDate')"
              />

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t('pages.admin-tracks-id-edit.submitButton')
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

  async asyncData({ app, params }) {
    const track = await app.$api.track.getById(params.id)
    return {
      loading: false,
      error: null,
      track,
      form: {
        name: track.name,
        name_english: track.name_english,
        starts_on: new Date(track.starts_on),
        ends_on: new Date(track.ends_on)
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.track
        .update(this.track.id, this.form)
        .then(() =>
          this.$router.push(
            this.localePath({
              name: 'admin-tracks-id-manage',
              params: { id: this.track.id }
            })
          )
        )
        .catch(this.handleGenericError)
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>
