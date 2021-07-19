<template>
  <el-dialog
    :visible="visible"
    :show-close="false"
    @close="closeDialog"
  >
    <bf-dialog-header
      slot="title"
      title="Select from various organs and systems to filter your results:"
      sub-title="Anatomical mappings for both humans and rats are available"
    />

    <dialog-body>
      <div>
        <el-button-group class="anatomy_toggle">
          <el-button
            :class="{ 'anatomy_toggle__active': entry === 'NCBITaxon:9606' }"
            v-on:click="() => setAnatomy('NCBITaxon:9606')"
          >
            Human
          </el-button>
          <el-button
            :class="{ 'anatomy_toggle__active': entry === 'NCBITaxon:10114' }"
            v-on:click="() => setAnatomy('NCBITaxon:10114')"
          >
            Rat
          </el-button>
        </el-button-group>
      </div>
      <div class="flatmap__wrapper">
        <client-only placeholder="Loading viewer...">
          <FlatmapVuer
            v-show="entry === 'NCBITaxon:9606'"
            entry="NCBITaxon:9606"
            height="100%"
            v-on:resource-selected="searchScaffoldLabel"
          />
          <FlatmapVuer
            v-show="entry === 'NCBITaxon:10114' "
            entry="NCBITaxon:10114"
            height="100%"
            v-on:resource-selected="searchScaffoldLabel"
          />
        </client-only>
      </div>
    </dialog-body>

  </el-dialog>
</template>

<script lang="ts">
  import Vue from 'vue'
  import BfDialogHeader from '@/components/bf-dialog-header/BfDialogHeader.vue'
  import DialogBody from '@/components/dialog-body/DialogBody.vue'
  import '@abi-software/flatmapvuer'
  import '@abi-software/flatmapvuer/dist/flatmapvuer.css'
  import BfButton from "~/components/shared/BfButton/BfButton.vue";

  interface Props {
    visible: boolean;
    onMapClick: (label: string) => void;
  }

  interface Methods {
    searchScaffoldLabel: (payload: { label: string }) => void
    closeDialog: () => void
    setAnatomy: (entry: FlatmapEntry) => void;
  }

  type FlatmapEntry = 'NCBITaxon:9606' | 'NCBITaxon:10114'

  interface Data {
    entry: FlatmapEntry
  }

  export default Vue.extend<Data, Methods, never, Props>({
    name: 'SearchMapPopup',

    components: {BfButton, BfDialogHeader, DialogBody },

    props: {
      visible: {
        type: Boolean,
        default: false
      },
      onMapClick: {
        type: Function
      }
    },

    data: () => ({
      entry: 'NCBITaxon:9606'
    }),

    methods: {
      searchScaffoldLabel: function(this: Props & Methods, payload) {
        this.onMapClick(payload.label)
        this.closeDialog()
      },

      /**
       * Closes the dialog
       */
      closeDialog: function(this: { $emit: (message: string, value: boolean ) => void }) {
        this.$emit('update:visible', false)
      },

      setAnatomy: function(this: Data, entry: FlatmapEntry) {
        this.entry = entry;
      }
    }
  })
</script>

<style lang="scss" scoped>
  @import '../../assets/_variables.scss';
  ::v-deep {
    .dialog-body,
    .el-dialog__body {
      font-size: inherit;
      padding-top: .5em;
    }
    .el-dialog__body {
      overflow: hidden;
      overflow-y: auto;
    }
  }
  h2 {
    font-size: 0.875em;
    font-weight: 500;
    margin-bottom: 1em;
  }
  h3 {
    color: #000;
    font-size: 0.75em;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 0.8125em;
  }
  ::v-deep .el-dialog {
    @media (max-width: 48em) {
      width: calc(100vw - 2em);
    }
  }
  .flatmap__wrapper {
    width:100%;
    height:512px;
    border: 1px solid $pudendal;
  }
  .anatomy_toggle {
    padding-bottom: .75em;
    button {
      width: 90px;
    }
    &__active {
      background-color: $median;
      color: $cochlear;
      &:focus,
      &:active {
        background-color: $median;
        color: $cochlear;
      }
    }
  }
</style>
