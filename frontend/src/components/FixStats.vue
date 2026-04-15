<template>
  <div class="fix-stats">
    <div class="stats-item">
      <el-icon class="stats-icon"><CircleCheckFilled /></el-icon>
      <span class="stats-label">Fixes:</span>
      <el-tag :type="fixCount > 0 ? 'success' : 'info'" size="small">
        {{ fixCount }}
      </el-tag>
    </div>
    <div class="stats-item" v-if="processingTime > 0">
      <el-icon class="stats-icon"><Timer /></el-icon>
      <span class="stats-label">Time:</span>
      <span class="stats-value">{{ processingTime }}ms</span>
    </div>
    <div class="stats-details" v-if="fixes.length > 0">
      <el-popover placement="top" :width="300" trigger="hover">
        <template #reference>
          <el-button text size="small">
            <el-icon><Document /></el-icon>
            View Details
          </el-button>
        </template>
        <div class="fix-details-list">
          <div v-for="(fix, index) in fixes" :key="index" class="fix-item">
            <div class="fix-header">
              <el-tag size="small" :type="getTypeColor(fix.type)">
                {{ fix.type }}
              </el-tag>
              <span class="fix-location">Line {{ fix.line }}, Col {{ fix.column }}</span>
            </div>
            <div class="fix-content">
              <span class="fix-original">{{ fix.original }}</span>
              <el-icon class="fix-arrow"><Right /></el-icon>
              <span class="fix-corrected">{{ fix.corrected }}</span>
            </div>
          </div>
        </div>
      </el-popover>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FixItem } from '../store'

interface Props {
  fixCount: number
  processingTime: number
  fixes: FixItem[]
}

withDefaults(defineProps<Props>(), {
  fixCount: 0,
  processingTime: 0,
  fixes: () => []
})

const getTypeColor = (type: string): 'success' | 'warning' | 'danger' | 'info' => {
  const colorMap: Record<string, 'success' | 'warning' | 'danger' | 'info'> = {
    'package': 'success',
    'function': 'warning',
    'class': 'danger',
    'module': 'info'
  }
  return colorMap[type] || 'info'
}
</script>

<style scoped>
.fix-stats {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stats-icon {
  font-size: 18px;
  color: #409eff;
}

.stats-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.stats-value {
  font-size: 14px;
  color: #303133;
  font-weight: 600;
}

.fix-details {
  margin-left: auto;
}

.fix-details-list {
  max-height: 300px;
  overflow-y: auto;
}

.fix-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.fix-item:last-child {
  border-bottom: none;
}

.fix-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.fix-location {
  font-size: 12px;
  color: #909399;
}

.fix-content {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}

.fix-original {
  color: #f56c6c;
  text-decoration: line-through;
}

.fix-arrow {
  color: #909399;
  font-size: 14px;
}

.fix-corrected {
  color: #67c23a;
  font-weight: 500;
}
</style>