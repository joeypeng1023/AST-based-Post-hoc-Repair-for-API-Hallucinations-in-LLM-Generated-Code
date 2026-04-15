<template>
  <el-button
    type="primary"
    size="large"
    :loading="loading"
    :disabled="disabled"
    @click="handleClick"
    class="fix-button"
  >
    <el-icon v-if="!loading"><MagicStick /></el-icon>
    <span v-if="!loading">Fix Code</span>
  </el-button>
</template>

<script setup lang="ts">
interface Props {
  loading: boolean
  disabled: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
  disabled: false
})

const emit = defineEmits<{
  (e: 'fix'): void
}>()

const handleClick = () => {
  emit('fix')
}
</script>

<style scoped>
.fix-button {
  font-weight: 500;
  padding: 12px 24px;
}

.fix-button :deep(.el-icon) {
  margin-right: 6px;
}
</style>