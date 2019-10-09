<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">
        {{ $t('inicio') }}
      </router-link>
    </div>
    <router-view />
  </div>
</template>

<style lang="scss">
</style>
