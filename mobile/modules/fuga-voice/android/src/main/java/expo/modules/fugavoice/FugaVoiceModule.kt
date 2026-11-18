package expo.modules.fugavoice

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import expo.modules.kotlin.Promise
import expo.modules.kotlin.functions.Queues
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition

class FugaVoiceModule : Module() {
  private var recognizer: SpeechRecognizer? = null
  private var pending: Promise? = null
  private val handler = Handler(Looper.getMainLooper())
  private var fallback = false
  private var generation = 0

  override fun definition() = ModuleDefinition {
    Name("FugaVoice")

    AsyncFunction("start") { promise: Promise ->
      val context = appContext.reactContext
      if (context == null || !SpeechRecognizer.isRecognitionAvailable(context)) {
        promise.reject("UNAVAILABLE", "Reconocimiento no disponible.", null)
      } else if (context.checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
        promise.reject("PERMISSION", "Permiso de micrófono requerido.", null)
      } else if (pending != null) {
        promise.reject("BUSY", "Ya hay una captura activa.", null)
      } else {
        pending = promise
        fallback = false
        listen("es-CO")
        handler.postDelayed({ recognizer?.stopListening() }, 30000)
        handler.postDelayed({ fail("TIMEOUT") }, 32000)
      }
    }.runOnQueue(Queues.MAIN)

    AsyncFunction("stop") { recognizer?.stopListening() }.runOnQueue(Queues.MAIN)
    AsyncFunction("cancel") { fail("CANCELLED") }.runOnQueue(Queues.MAIN)
    OnActivityEntersBackground { handler.post { fail("CANCELLED") } }
    OnDestroy { handler.post { fail("CANCELLED") } }
  }

  private fun listen(locale: String) {
    val context = appContext.reactContext ?: return fail("UNAVAILABLE")
    val currentGeneration = ++generation
    try {
      recognizer?.destroy()
      recognizer = SpeechRecognizer.createSpeechRecognizer(context)
      recognizer?.setRecognitionListener(object : RecognitionListener {
        override fun onResults(results: Bundle?) {
          if (currentGeneration != generation) return
          val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull().orEmpty()
          val promise = pending
          pending = null
          cleanup()
          promise?.resolve(text.take(280))
        }
        override fun onError(error: Int) {
          if (currentGeneration != generation) return
          if (!fallback && (error == 12 || error == 13)) {
            fallback = true
            listen("es")
          } else fail("RECOGNITION_ERROR")
        }
        override fun onReadyForSpeech(params: Bundle?) {}
        override fun onBeginningOfSpeech() {}
        override fun onRmsChanged(rmsdB: Float) {}
        override fun onBufferReceived(buffer: ByteArray?) {}
        override fun onEndOfSpeech() {}
        override fun onPartialResults(partialResults: Bundle?) {}
        override fun onEvent(eventType: Int, params: Bundle?) {}
      })
      recognizer?.startListening(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        putExtra(RecognizerIntent.EXTRA_LANGUAGE, locale)
        putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
        putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
      })
    } catch (_: Exception) { fail("UNAVAILABLE") }
  }

  private fun fail(code: String) {
    val promise = pending
    pending = null
    cleanup()
    promise?.reject(code, "Puedes registrar el gasto por texto.", null)
  }
  private fun cleanup() {
    generation++
    handler.removeCallbacksAndMessages(null)
    val current = recognizer
    recognizer = null
    current?.cancel()
    current?.destroy()
  }
}
