<template>
  <div class="search-form" @keyup.enter="$emit('search')">
    <div class="input-wrap">
      <input :value="value" placeholder="Enter search criteria" @input="$emit('input', $event.target.value)" />
      <button v-if="q" class="btn-clear-search" @click="$emit('clear')">
        <svg-icon
          name="icon-clear"
          stroke="red"
          color="#909399 #fff"
          height="22"
          width="22"
        />
      </button>
    </div>
    <el-button class="btn-submit-search" @click="$emit('search')">
      <svg-icon
        icon="icon-magnifying-glass"
        height="25"
        width="25"
        dir="left"
      />
      <span>
        Search
      </span>
    </el-button>
  </div>
</template>

<script>
export default {
  name: 'SearchForm',

  props: {
    value: {
      type: String,
      default: ''
    },
    q: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

.search-form {
  display: flex;
  width: 100%;
}
.input-wrap {
  display: flex;
  position: relative;
  width: 100%;
  border: .05rem solid black;
  border-radius: .2rem;
  margin: 0 .5rem;
}
input {
  background: #fff;
  border-radius: .2rem;
  box-sizing: border-box;
  border: none;
  color: #909399;
  flex: 1;
  font-size: 0.875rem;
  outline: none;
  margin: 0;
  padding: 0.5rem 2.25rem 0.5rem 0.8125rem;
  &:focus {
    border-color: $median;
  }
  &::-ms-clear {
    display: none;
  }
}
.btn-clear-search {
  background: none;
  border: none;
  cursor: pointer;
  height: 100%;
  outline: none;
  margin: 0;
  position: absolute;
  right: 0;
  top: 0;
  &:hover,
  &:active {
    opacity: 0.75;
  }
}
.btn-submit-search {
  background: $median;
  color: white;
  border: 1px solid $median;
  border-radius: 4px;
  cursor: pointer;
  height: 2.5rem;
  padding: 0 1.5rem;
  @media screen and (max-width: 28rem) {
    padding: 0 .5rem;
    span {
      display: none;
    }
  }
}
.clear-search {
  background-color: transparent;
  display: inline-block;
  border: none;
  width: fit-content;
  color: $cochlear;
  font-size: 1rem;
  font-family: $font-family;
}
</style>
