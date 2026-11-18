import 'react-native-url-polyfill/auto';
import { createClient, processLock } from '@supabase/supabase-js';
import { AppState, Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { createWebAuthStorage } from '../auth/callback';
import { isPublicSupabaseKey, isSupabaseRoot } from './publicConfig';

const url = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const key = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';
export const authConfigured = isSupabaseRoot(url) && isPublicSupabaseKey(key);
// Chunk sessions: native SecureStore has per-item size limits on some devices.
const webStorage = createWebAuthStorage(() => typeof localStorage !== 'undefined' ? localStorage : null);
const storage = {
  async getItem(name:string) {
    if (Platform.OS === 'web') return webStorage.getItem(name);
    const count = Number(await SecureStore.getItemAsync(name + '.count') || 0);
    if (!count || count > 100) return null;
    const parts = await Promise.all(Array.from({length:count}, (_,i) => SecureStore.getItemAsync(name+'.'+i)));
    return parts.every(p => p !== null) ? parts.join('') : null;
  },
  async setItem(name:string, value:string) {
    if (Platform.OS === 'web') { await webStorage.setItem(name,value); return; }
    const oldCount = Number(await SecureStore.getItemAsync(name+'.count') || 0);
    const chunks = value.match(/[\s\S]{1,1500}/g) || [];
    // Publish the count only after all chunks are stored.
    await Promise.all(chunks.map((chunk,i) => SecureStore.setItemAsync(name+'.'+i,chunk)));
    await SecureStore.setItemAsync(name+'.count',String(chunks.length));
    await Promise.all(Array.from({length:Math.max(0,oldCount-chunks.length)},(_,i) => SecureStore.deleteItemAsync(name+'.'+(i+chunks.length))));
  },
  async removeItem(name:string) {
    if (Platform.OS === 'web') { await webStorage.removeItem(name); return; }
    const count = Math.min(100,Number(await SecureStore.getItemAsync(name+'.count') || 0));
    await SecureStore.deleteItemAsync(name+'.count');
    await Promise.all(Array.from({length:count},(_,i)=>SecureStore.deleteItemAsync(name+'.'+i)));
  },
};
export const supabase = createClient(authConfigured ? url : 'https://not-configured.invalid', authConfigured ? key : 'not-configured', {
  auth: { storage, autoRefreshToken:true, persistSession:true, detectSessionInUrl:false, flowType:'pkce', lock:processLock },
});
if (Platform.OS !== 'web') {
  AppState.addEventListener('change', state => {
    if (state === 'active') supabase.auth.startAutoRefresh();
    else supabase.auth.stopAutoRefresh();
  });
}
