require 'bundler/setup'
require 'active_support/inflector'
require 'translit'
require 'digest'

def transliterate_with_fallback(text)
  # оригинал механизма тут - NestingUniqueHeadCounter#header
  transliterated_text = Translit.convert(text, :english).gsub(/<[^>]*>/, "").parameterize
  if transliterated_text.empty?
    transliterated_text = Digest::MD5.hexdigest(text)
  end
  transliterated_text
end

# Какой заголовок преобразовать в относительную ссылку
texts = [
  "Активация приложения на аккаунте",
  "Деактивация приложения на аккаунте",
  "Проверка статуса активации приложения в системе разработчика"
]

texts.each do |text|
  result = transliterate_with_fallback(text)
  puts "#{text} => #{result}"
end
