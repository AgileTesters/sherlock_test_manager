<template>
  <div
    class="dropdown is-right"
    @click="showCaseMenu = !showCaseMenu"
    v-bind:class="{ 'is-active': showCaseMenu }"
  >
    <div class="dropdown-trigger">
      <button>
        <i class="far fa-ellipsis-v"></i>
      </button>
    </div>
    <div class="dropdown-menu" id="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <a href="#" class="dropdown-item">
          edit
        </a>
        <a class="dropdown-item">
          block
        </a>
        <hr class="dropdown-divider" />
        <a href="#" class="dropdown-item">
          delete
        </a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      showCaseMenu: false
    };
  },
  methods: {
    seila() {
      console.log(this.showCaseMenu);
    }
  },
  mounted() {}
};
</script>
<style></style>
