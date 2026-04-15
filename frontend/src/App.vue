<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">
          <el-icon class="title-icon"><Edit /></el-icon>
          Code Fix Tool
        </h1>
        <p class="app-description">
          Detect and fix API hallucinations in LLM-generated code
        </p>
      </div>
      <div class="header-actions">
        <FixButton 
          @fix="handleFix" 
          :loading="store.isLoading"
          :disabled="!store.originalCode.trim()"
        />
        <el-switch
          v-model="autoFixEnabled"
          class="auto-fix-switch"
          inline-prompt
          active-text="Auto"
          inactive-text="Manual"
        />
      </div>
    </header>

    <main class="app-main">
      <div class="editor-container">
        <div class="editor-panel">
          <div class="panel-header">
            <el-icon><Edit /></el-icon>
            <span>Original Code</span>
          </div>
          <CodeEditor 
            v-model="store.originalCode"
            language="python"
            :readonly="false"
            @change="handleCodeChange"
          />
        </div>
        <div class="editor-panel">
          <div class="panel-header">
            <el-icon><Check /></el-icon>
            <span>Fixed Code</span>
          </div>
          <CodeEditor 
            v-model="store.fixedCode"
            language="python"
            :readonly="true"
            :highlights="store.fixes"
          />
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <FixStats 
        :fix-count="store.fixCount"
        :processing-time="store.processingTime"
        :fixes="store.fixes"
      />
      <el-alert
        v-if="store.error"
        type="error"
        :closable="true"
        @close="store.setError(null)"
        show-icon
      >
        {{ store.error }}
      </el-alert>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCodeStore } from './store'
import FixButton from './components/FixButton.vue'
import CodeEditor from './components/CodeEditor.vue'
import FixStats from './components/FixStats.vue'
import axios from 'axios'

const store = useCodeStore()
const autoFixEnabled = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

const handleCodeChange = () => {
  if (autoFixEnabled.value && store.originalCode.trim()) {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
    }
    debounceTimer = setTimeout(() => {
      handleFix()
    }, 1000)
  }
}

const handleFix = async () => {
  if (!store.originalCode.trim()) return

  store.setLoading(true)
  store.setError(null)
  const startTime = Date.now()

  try {
    const response = await axios.post('/api/fix', {
      code: store.originalCode
    })

    const data = response.data
    store.setFixedCode(data.fixed_code)
    store.setFixes(data.fixes)
    store.setProcessingTime(Date.now() - startTime)
  } catch (err: any) {
    store.setError(
      err.response?.data?.detail || 
      err.message || 
      'Failed to connect to the backend service. Please ensure the server is running.'
    )
  } finally {
    store.setLoading(false)
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.app-description {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.auto-fix-switch {
  margin-left: 8px;
}

.app-main {
  flex: 1;
  padding: 16px;
  overflow: hidden;
}

.editor-container {
  display: flex;
  gap: 16px;
  height: 100%;
}

.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
  font-weight: 500;
  color: #606266;
  font-size: 14px;
}

.panel-header .el-icon {
  color: #409eff;
}

.app-footer {
  padding: 12px 24px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-footer :deep(.el-alert) {
  flex: 1;
  margin: 0;
}
</style>