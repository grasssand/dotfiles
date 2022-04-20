function! myspacevim#before() abort
    let g:neoformat_enabled_python = ['black']
endfunction

function! myspacevim#after() abort
    iunmap jk
endfunction
