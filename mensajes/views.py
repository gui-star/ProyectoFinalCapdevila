from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm

@login_required
def message_list(request):
    messages_received = Message.objects.filter(receiver=request.user)
    return render(request, 'lista_mensajes.html', {'messages': messages_received})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Mensaje enviado con éxito')
            return redirect('mensajes:lista_mensajes')
    else:
        form = MessageForm()
    
    return render(request, 'enviar_mensaje.html', {'form': form})



@login_required
def view_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    # Marcar el mensaje como leído si el receptor es el usuario actual
    if message.receiver == request.user:
        message.is_read = True
        message.save()
    return render(request, 'ver_mensaje.html', {'message': message})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    
    # Verificar que el usuario actual sea el receptor del mensaje
    if message.receiver == request.user:
        message.delete()
        messages.success(request, 'Mensaje eliminado con éxito')
    else:
        messages.error(request, 'No tienes permisos para eliminar este mensaje')
    
    return redirect('mensajes:lista_mensajes')