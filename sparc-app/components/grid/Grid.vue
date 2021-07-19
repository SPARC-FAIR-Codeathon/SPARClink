<template>
  <el-row :gutter="20" type="flex" class="cards">
    <el-col
      v-for="card in cards"
      :key="card.key"
      class="cards-col"
      :xs="24"
      :sm="12"
      :md="8"
      :lg="6"
    >
      <div class="card">
        <div class="card-top">
          <nuxt-link
            :to="{
              name: onClickRoute,
              params: {
                datasetId: card.id
              }
            }"
          >
            <dataset-banner-image :src="card.banner" />
          </nuxt-link>

          <h3 class="title">
            {{ card.name }}
          </h3>
          <p class="description">
            {{ card.description }}
          </p>
        </div>
        <div class="card-bottom">
          <div class="link">
            <nuxt-link
              no-prefetch
              :to="{
                name: onClickRoute,
                params: {
                  datasetId: card.id
                }
              }"
            >
              Explore Dataset
            </nuxt-link>
            <a :href="card.href">{{ card.cta }}</a>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import DatasetBannerImage from '@/components/DatasetBannerImage/DatasetBannerImage.vue'

export default {
  name: 'Grid',

  components: {
    DatasetBannerImage
  },

  props: {
    cards: {
      type: Array,
      default: () => []
    },
    cardType: {
      type: String,
      default: ''
    }
  },

  computed: {
    onClickRoute: function() {
      if (this.cardType == 'datasets') {
        return 'datasets-datasetId'
      } else if (this.cardType == 'sim_models') {
        return 'workflows-datasetId'
      } else {
        return 'datasets-datasetId'
      }
    }
  }
}
</script>

<style lang="scss"></style>

<style lang="scss" scoped>
.cards {
  display: flex;
  flex-wrap: wrap;
}

.cards-col {
  display: flex;
}

.card {
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  box-sizing: border-box;
  margin-bottom: 20px;
  flex: 1 1 100%;
  padding: 2.5rem 1.8rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .title {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    word-break: break-word;
  }

  .description {
    font-size: 0.9rem;
    line-height: 1rem;
    color: #303133;
    margin-bottom: 1rem;
  }

  .link {
    a {
      text-decoration: none;
      text-transform: uppercase;
      color: #8300bf;
    }
  }
}

.dataset-image {
  height: auto;
  width: 100%;
}

@media screen and (min-width: 40em) {
  .card {
    flex: 1 1 calc(50% - 2em);
  }
}
@media screen and (min-width: 60em) {
  .card {
    flex: 1 1 calc(25% - 2em);
  }
}
</style>
