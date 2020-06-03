$('.hideo').click(function(){ $('.history_block').addClass('scrolled')})

$('.hideo').click(function(){ $('.history_block_out').addClass('scrolled-out')})

$('.history_block_out').click(function(){ $('.history_block').removeClass('scrolled')})

$('.history_block_out').click(function(){ $('.history_block_out').removeClass('scrolled-out')})

$('.close-top-btn').click(function(){ $('.modal-search').removeClass('activated')})