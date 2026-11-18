package expo.modules.fugawindowinsets

import android.content.Context
import android.os.Build
import android.util.DisplayMetrics
import android.view.ViewTreeObserver
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsAnimationCompat
import androidx.core.view.WindowInsetsCompat
import expo.modules.kotlin.AppContext
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition
import expo.modules.kotlin.viewevent.EventDispatcher
import expo.modules.kotlin.views.ExpoView

class FugaWindowInsetsModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("FugaWindowInsets")
    View(FugaWindowInsetsView::class) {
      Events("onInsetsChange")
      Prop("viewportWidth") { view: FugaWindowInsetsView, value: Double ->
        view.viewportWidth = value
        view.post { view.reportInsets() }
      }
      Prop("viewportHeight") { view: FugaWindowInsetsView, value: Double ->
        view.viewportHeight = value
        view.post { view.reportInsets() }
      }
    }
  }
}

/** Observes only this public screen; never replaces a listener on the activity/root. */
class FugaWindowInsetsView(context: Context, appContext: AppContext) :
  ExpoView(context, appContext), ViewTreeObserver.OnGlobalLayoutListener {
  val onInsetsChange by EventDispatcher()
  var viewportWidth = 0.0
  var viewportHeight = 0.0
  private var lastPayload: Map<String, Any>? = null

  override fun onAttachedToWindow() {
    super.onAttachedToWindow()
    viewTreeObserver.addOnGlobalLayoutListener(this)
    ViewCompat.setOnApplyWindowInsetsListener(this) { _, insets ->
      reportInsets(insets)
      insets // Do not consume or change other views' insets.
    }
    ViewCompat.setWindowInsetsAnimationCallback(this,
      object : WindowInsetsAnimationCompat.Callback(DISPATCH_MODE_CONTINUE_ON_SUBTREE) {
        override fun onProgress(
          insets: WindowInsetsCompat,
          animations: MutableList<WindowInsetsAnimationCompat>
        ): WindowInsetsCompat {
          reportInsets(insets)
          return insets
        }
      })
    post { reportInsets() }
    ViewCompat.requestApplyInsets(this)
  }

  override fun onDetachedFromWindow() {
    if (viewTreeObserver.isAlive) viewTreeObserver.removeOnGlobalLayoutListener(this)
    ViewCompat.setOnApplyWindowInsetsListener(this, null)
    ViewCompat.setWindowInsetsAnimationCallback(this, null)
    lastPayload = null
    super.onDetachedFromWindow()
  }

  override fun onGlobalLayout() = reportInsets()

  fun reportInsets(value: WindowInsetsCompat? = null) {
    if (!isAttachedToWindow || viewportWidth <= 0 || viewportHeight <= 0) return
    val activity = appContext.currentActivity ?: return
    val insets = value ?: ViewCompat.getRootWindowInsets(this) ?: return
    val density = resources.displayMetrics.density.toDouble()
    val bars = insets.getInsets(
      WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
    val ime = insets.getInsets(WindowInsetsCompat.Type.ime())
    val origin = IntArray(2)
    getLocationInWindow(origin)
    val windowWidth: Int
    val windowHeight: Int
    if (Build.VERSION.SDK_INT >= 30) {
      val bounds = activity.windowManager.currentWindowMetrics.bounds
      windowWidth = bounds.width()
      windowHeight = bounds.height()
    } else {
      val metrics = DisplayMetrics()
      @Suppress("DEPRECATION")
      activity.windowManager.defaultDisplay.getRealMetrics(metrics)
      windowWidth = metrics.widthPixels
      windowHeight = metrics.heightPixels
    }
    val payload = mapOf<String, Any>(
      "systemTop" to bars.top / density, "systemBottom" to bars.bottom / density,
      "systemLeft" to bars.left / density, "systemRight" to bars.right / density,
      "imeBottom" to ime.bottom / density,
      "keyboardVisible" to insets.isVisible(WindowInsetsCompat.Type.ime()),
      "frameTop" to origin[1] / density, "frameLeft" to origin[0] / density,
      "viewportWidth" to viewportWidth, "viewportHeight" to viewportHeight,
      "windowWidth" to windowWidth / density, "windowHeight" to windowHeight / density)
    if (payload != lastPayload) {
      lastPayload = payload
      onInsetsChange(payload)
    }
  }
}
