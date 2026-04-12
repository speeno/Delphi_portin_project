/**
 * 스캐너 입력 컴포넌트
 *
 * HID 키보드 웨지 방식 바코드 스캐너 입력을 처리한다.
 * - 빠른 연속 입력 감지 (스캐너 vs 수동 입력 구분)
 * - 접두/접미 문자 처리
 * - 포커스 관리
 */

export class ScannerInput {
  constructor(options = {}) {
    this.onScan = options.onScan || (() => {});
    this.scanThresholdMs = options.scanThresholdMs || 50;
    this.suffixChar = options.suffixChar || 'Enter';
    this.buffer = '';
    this.lastKeyTime = 0;
    this.isScanning = false;
  }

  attach(inputElement) {
    this.element = inputElement;

    inputElement.addEventListener('keydown', (e) => {
      const now = Date.now();
      const timeDiff = now - this.lastKeyTime;

      if (e.key === this.suffixChar) {
        e.preventDefault();
        if (this.buffer.length > 2 && this.isScanning) {
          this.onScan(this.buffer);
          inputElement.value = '';
        } else if (inputElement.value) {
          this.onScan(inputElement.value);
          inputElement.value = '';
        }
        this.buffer = '';
        this.isScanning = false;
        return;
      }

      if (e.key.length === 1) {
        if (timeDiff < this.scanThresholdMs && this.buffer.length > 0) {
          this.isScanning = true;
        }
        this.buffer += e.key;
        this.lastKeyTime = now;
      }
    });
  }

  focus() {
    if (this.element) this.element.focus();
  }

  detach() {
    this.element = null;
  }
}

export function renderScannerInput({ id, label, placeholder }) {
  return `
    <div class="scanner-input-group">
      <label for="${id}">${label}</label>
      <div class="scanner-input-wrapper">
        <input type="text" id="${id}" class="scanner-input" placeholder="${placeholder || '바코드 스캔 또는 직접 입력'}" autocomplete="off" />
        <span class="scanner-icon">📷</span>
      </div>
    </div>`;
}
