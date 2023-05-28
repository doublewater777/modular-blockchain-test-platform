<template>
  <div id="app">
    <plat-form-vue></plat-form-vue>
  </div>
</template>

<script>
import PlatFormVue from './components/PlatForm.vue';
export default {
  name: 'App',
  components: {
    PlatFormVue
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
